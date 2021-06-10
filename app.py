from flask import request
import telegram
from tracker_bot.mastermind import mainCommandHandler
from tracker_bot.credentials import URL, reset_key, bot_token, bot_user_name

from tracker_app import create_app

# https://api.telegram.org/bot1359229669:AAEm8MG26qbA9XjJyojVKvPI7jAdMVqAkc8/getMe


bot = telegram.Bot(token=bot_token)

app = create_app()

TOKEN = bot_token


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
        mainCommandHandler(incoming_message=update.messagem, telebot_instance=bot)

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


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True, debug=True, ssl_context='adhoc')
