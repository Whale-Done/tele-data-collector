import json

from flask import request, make_response
import telegram

from tracker_bot.mastermind import main_command_handler
from tracker_bot.credentials import DEPLOY_URL, reset_key, deploy_bot_token, debug_bot_token, DEBUG_URL
from tracker_app import app, db, redis_client
from appconfig import AppConfig
from flask import Flask
from threading import Thread
from time import sleep

# from flask_assets import Environment, Bundle

# assets = Environment(app)
# css = Bundle('tailwind.css', output='dist/tailwind.css', filters='postcss',)

# assets.register('css', css)
# css.build()


my_logs_keyboard_buttons = [[telegram.KeyboardButton('list view')],
                            [telegram.KeyboardButton('spending stats')],
                                   [telegram.KeyboardButton('back to home')]]
my_logs_keyboard_markup = telegram.ReplyKeyboardMarkup(my_logs_keyboard_buttons)


debug = AppConfig.debug

if debug:
    URL = DEBUG_URL
    TOKEN = debug_bot_token
    bot = telegram.Bot(token=debug_bot_token)
else:
    URL = DEPLOY_URL
    TOKEN = deploy_bot_token
    bot = telegram.Bot(token=deploy_bot_token)


class ExpenseEntry(db.Model):
    __tablename__ = "entries"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    amount = db.Column(db.String(128))
    category = db.Column(db.String(128))
    description = db.Column(db.String(128))
    datetime = db.Column(db.String(128))
    submit_time = db.Column(db.String(128))
    type = db.Column(db.String(128))

    # def __init__(self, username, amount, category, description, datetime, submit_time, type):
    # def __init__(self):
    # self.username = username
    # self.amount = amount
    # self.category = category
    # self.description = description
    # self.datetime = datetime
    # self.submit_time = submit_time
    # self.type = type


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to the Telegram object
    print("Received message")
    # for overwhelming updates, clear the update attemp (this line below)
    # and have the method return 1 to clear all pending updates
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
    except:
        print("some error has occured internally")

    if update.message:
        chat_id = update.message.chat.id
        
        # keep track of chat_id for notification
        if redis_client.get("chatids") is not None:
            current_subscription = json.loads(redis_client.get("chatids"))
            if chat_id not in current_subscription:
                current_subscription.append(chat_id)
        else:
            current_subscription = [chat_id]

        redis_client.set("chatids", json.dumps(current_subscription))

        state = main_command_handler(incoming_message=update.message, telebot_instance=bot, redis_client=redis_client,
                                     db=db)
        if state is not None:
            username = update.message.from_user['username']
            chat_id = update.message.chat.id
            msg_id = update.message.message_id
            if state == "user_query_stats":
                rs = db.engine.execute(f'''
                    SELECT COUNT(*) as count, type FROM entries
                    WHERE
                        username='{username}'
                    GROUP BY
                        type
                    ''')

                replyList = ""

                # Diagnostic feature
                TARGET_COUNT = 25
                entries = ExpenseEntry.query.filter(ExpenseEntry.username == username).order_by(ExpenseEntry.datetime.desc()).all()
                expense_detail_list = [{
                    'amount': entry.amount,
                    'category': entry.category,
                    'description': entry.description,
                    'purchase_type': entry.type,
                    'submit_time': entry.submit_time,
                    'expense_time': entry.datetime,
                }
                    for entry in entries]

                current_count = len(expense_detail_list)
                
                for entry in rs:
                    replyList += f"{entry.type} ||| count: {entry.count}\n"

                # if target count not met, send this
                if current_count <= TARGET_COUNT:
                    required_count = TARGET_COUNT - current_count

                    bot.sendMessage(chat_id=chat_id, text=f"Let's see... \n\nwe still need {required_count} more entries to give you a more accurate report. \n\nBut your current stats are -\n{replyList}",
                                            reply_to_message_id=msg_id, reply_markup=my_logs_keyboard_markup)
                else:        
                    # target count is met, send a more detailed report
                    bot.sendMessage(chat_id=chat_id, text=f"Your stats -\n{replyList}",
                                            reply_to_message_id=msg_id, reply_markup=my_logs_keyboard_markup)
                                            
                redis_client.set(username + "state", "user_query_logs")
            else:
                redis_client.set(username + "state", state)

    return 'ok'


@app.route('/{}'.format(reset_key), methods=['POST'])
def reset():
    return 'ok'


@app.route("/test-create", methods=['GET'])
def test_create():
    db_entry = ExpenseEntry()
    db_entry.username = "test"
    db_entry.amount = "test"
    db_entry.category = "test"
    db_entry.datetime = "test"
    db_entry.description = "test"
    db_entry.type = "test"
    db_entry.submit_time = "test"

    db.session.add(db_entry)
    db.session.commit()
    return 'created'


@app.route("/test-redis", methods=['GET'])
def test_redis():
    print(redis_client)
    return 'redis ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/resetupdate', methods=['GET', 'POST'])
def reset_update():
    """
    Really a temprorary method to keep the update from flooding
    """
    s = bot.setWebhook('{URL}{RESET}'.format(URL=URL, RESET=reset_key))
    if s:
        return "reset hook setup ok"
    else:
        return "reset hook setup failed"


@app.route('/dropwebhook', methods=['GET'])
def drop_webhook():
    """
    Stops the webhook from polling the server and drops all pending requests
    """
    s = bot.deleteWebhook(drop_pending_updates=True)

    if s:
        return "web hook delete success"
    else:
        return "web hook delete failure"


@app.route('/createall', methods=['GET'])
def create_db_table():
    db.create_all()
    return "Created entries"


@app.route('/get-entries', methods=['GET'])
def get_entries():
    entries = ExpenseEntry.query.order_by(ExpenseEntry.submit_time.desc()).all()
    expense_detail_list = [{
        'username': entry.username,
        'amount': entry.amount,
        'category': entry.category,
        'description': entry.description,
        'purchase_type': entry.type,
        'submit_time': entry.submit_time,
        'expense_time': entry.datetime,
    }
        for entry in entries]
    return make_response(json.dumps(expense_detail_list), 200)


@app.route('/notifyall', methods=['GET'])
def notify_all():
    if redis_client.get("chatids") is not None:
        list_of_chats = json.loads(redis_client.get("chatids"))

        for id in list_of_chats: 
            bot.send_message(id, "Hello! This is Whale calling for you to record your expense 🐳 \n\nHave a good one! 🤩")

    return make_response("Notified", 200)


@app.route('/clear_noti_targets', methods=['GET'])
def delete_targets():
    redis_client.delete("chatids")

    return make_response("Notified", 200)

# def schedule_checker():
#     while True:
#         schedule.run_pending()
#         sleep(1)

# def function_to_run():
#     return bot.send_message(some_id, "This is a message to send.")

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    # flask run --host=0.0.0.0
    # http://172.31.111.25:5000/
    # ./ngrok http 172.31.111.25:5000
    app.run(threaded=True, debug=False)
