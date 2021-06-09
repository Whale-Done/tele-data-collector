import redis

from flask import request, Flask
import telegram
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from tracker_bot.mastermind import mainCommandHandler
from tracker_bot.credentials import URL, reset_key, bot_token

app = Flask(__name__)
redis_client = FlaskRedis(app)

# redis_client.set('potato',1)
# print(redis_client.get('potato'))
# redis_client.delete('potato')

from tracker_app import create_app

# https://api.telegram.org/bot1359229669:AAEm8MG26qbA9XjJyojVKvPI7jAdMVqAkc8/getMe


bot = telegram.Bot(token=bot_token)

app = create_app()
db = SQLAlchemy(app)
TOKEN = bot_token

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
        state = mainCommandHandler(incoming_message=update.message, telebot_instance=bot, redis_client=redis_client)
        if state is not None:
            username = update.message.from_user['username']
            redis_client.set(username + "state", state)

    return 'ok'


# @app.route('/{}'.format(RESETKEY), methods=['POST'])
# def reset():
#     return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=bot_token))
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
    return "Created"


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    # flask run --host=0.0.0.0
    # http://172.31.111.25:5000/
    # ./ngrok http 172.31.111.25:5000
    app.run(threaded=True, debug=False)