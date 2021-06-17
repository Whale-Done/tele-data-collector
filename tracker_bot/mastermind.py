import json
import telegram
import logging
import pytz

from datetime import datetime
from .model import ExpenseEntry, UserAction
from .credentials import DEPLOY_URL, DEBUG_URL
from appconfig import AppConfig

if AppConfig.debug:
    URL = DEBUG_URL
else:
    URL = DEPLOY_URL

singapore=pytz.timezone('Asia/Singapore')
gmt=pytz.timezone('Etc/GMT')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

start_keyboard_buttons = [[telegram.KeyboardButton('create expense')], [telegram.KeyboardButton('my logs')]]
start_keyboard_markup = telegram.ReplyKeyboardMarkup(start_keyboard_buttons)

info_keyboard_buttons = [[telegram.KeyboardButton('view my info')], [telegram.KeyboardButton('enter my info')],
                         [telegram.KeyboardButton('home')]]
info_keyboard_markup = telegram.ReplyKeyboardMarkup(info_keyboard_buttons)

info_input_keyboard_buttons = [[telegram.KeyboardButton('skips')], [telegram.KeyboardButton('home')]]
info_input_keyboard_markup = telegram.ReplyKeyboardMarkup(info_input_keyboard_buttons)

delete_keyboard_buttons = [[telegram.KeyboardButton('confirm delete')],
                           [telegram.KeyboardButton('cancel delete')]]
delete_keyboard_markup = telegram.ReplyKeyboardMarkup(delete_keyboard_buttons)

amount_keyboard_buttons = [[telegram.KeyboardButton('less than 1')], [telegram.KeyboardButton('around 5')],
                           [telegram.KeyboardButton('cancel create')]]
amount_keyboard_markup = telegram.ReplyKeyboardMarkup(amount_keyboard_buttons)

category_keyboard_buttons = [[telegram.KeyboardButton('food'), telegram.KeyboardButton('drinks')],
                            [telegram.KeyboardButton('snacks'), telegram.KeyboardButton('transportation')],
                            [telegram.KeyboardButton('hobbies'), telegram.KeyboardButton('subscription/top up')],
                             [telegram.KeyboardButton('cancel create')]]
category_keyboard_markup = telegram.ReplyKeyboardMarkup(category_keyboard_buttons)

date_keyboard_buttons = [[telegram.KeyboardButton('Now (Or recent)'), telegram.KeyboardButton('Today morning')], [telegram.KeyboardButton('Today noon'), telegram.KeyboardButton('Today evening')], [telegram.KeyboardButton('cancel create')]]
date_keyboard_markup = telegram.ReplyKeyboardMarkup(date_keyboard_buttons)

item_name_keyboard_buttons = [[telegram.KeyboardButton('None (Leave blank)')],
                              [telegram.KeyboardButton('cancel create')]]
item_name_keyboard_markup = telegram.ReplyKeyboardMarkup(item_name_keyboard_buttons)

purchase_type_keyboard_buttons = [[telegram.KeyboardButton('1 (Pure Want)'),telegram.KeyboardButton('2')],
                                [telegram.KeyboardButton('3'),telegram.KeyboardButton('4')],
                                [telegram.KeyboardButton('5 (Real need!)'),telegram.KeyboardButton('cancel create')]]
purchase_type_keyboard_markup = telegram.ReplyKeyboardMarkup(purchase_type_keyboard_buttons)

confirm_create_keyboard_buttons = [[telegram.KeyboardButton('confirm create')],
                                   [telegram.KeyboardButton('cancel create')]]
confirm_create_keyboard_markup = telegram.ReplyKeyboardMarkup(confirm_create_keyboard_buttons)

my_logs_keyboard_buttons = [[telegram.KeyboardButton('list view')],
                            [telegram.KeyboardButton('spending stats')],
                                   [telegram.KeyboardButton('back to home')]]
my_logs_keyboard_markup = telegram.ReplyKeyboardMarkup(my_logs_keyboard_buttons)

kuala_lumpur=pytz.timezone('Asia/Kuala_Lumpur')

def main_command_handler(incoming_message, telebot_instance, redis_client, db):
    """Echo the user message."""
    chat_id = incoming_message.chat.id
    msg_id = incoming_message.message_id
    user = incoming_message.from_user
    username = user['username']

    text = incoming_message.text.encode('utf-8').decode()

    # check if current user has state
    if redis_client.get(user['username'] + "state") is not None:
        if text == "cancel delete" or text == "cancel create" or text == "back to home" or text == "/home":
            redis_client.delete(user['username'] + "state")
            telebot_instance.sendMessage(chat_id=chat_id, text="What would you like to do",
                                         reply_to_message_id=msg_id, reply_markup=start_keyboard_markup)
            return

        # step 1 of creating an expense entry
        state = redis_client.get(user['username'] + "state").decode('utf-8')
        print("state:" + state)

        if state == "user_enter_amount":
            telebot_instance.sendMessage(chat_id=chat_id, text="When did you make this expense",
                                         reply_to_message_id=msg_id, reply_markup=date_keyboard_markup)
            current_data_string = json.dumps({'username': user['username'], 'amount': text})
            redis_client.set(user['username'], current_data_string)

            return "user_enter_date"

        elif state == "user_enter_date":
            telebot_instance.sendMessage(chat_id=chat_id, text="enter the category of your expense",
                                         reply_to_message_id=msg_id, reply_markup=category_keyboard_markup)
            this_entry_obj = json.loads(redis_client.get(user['username']))
            now = datetime.now()
            if text == "Now (Or recent)":
                dt_string = now.astimezone(singapore).strftime("%d/%m/%Y %H:%M:%S")
            elif text == "Today morning":
                today_morning = datetime(now.year, now.month, now.day, 9,0,0)
                dt_string = today_morning.strftime("%d/%m/%Y %H:%M:%S")
            elif text == "Today noon":
                today_noon = datetime(now.year, now.month, now.day, 12,0,0)
                dt_string = today_noon.strftime("%d/%m/%Y %H:%M:%S")
            elif text == "Today evening":
                today_evening = datetime(now.year, now.month, now.day, 21,0,0)
                dt_string = today_evening.strftime("%d/%m/%Y %H:%M:%S")
            else:
                dt_string = text

            this_entry_obj['datetime'] = dt_string
            redis_client.set(user['username'], json.dumps(this_entry_obj))

            return "user_enter_category"

        elif state == "user_enter_category":
            telebot_instance.sendMessage(chat_id=chat_id, text="What item/service did you purchase? \n\nUse /home to go back",
                                         reply_to_message_id=msg_id, reply_markup=telegram.ReplyKeyboardRemove(remove_keyboard=True))

            this_entry_obj = json.loads(redis_client.get(user['username']))
            this_entry_obj['category'] = text
            redis_client.set(user['username'], json.dumps(this_entry_obj))

            return "user_enter_name"

        # original
        # elif state == "user_enter_name":
        #     telebot_instance.sendMessage(chat_id=chat_id, text="Classify your expense",
        #                                  reply_to_message_id=msg_id, reply_markup=purchase_type_keyboard_markup)

        #     this_entry_obj = json.loads(redis_client.get(user['username']))
        #     this_entry_obj['description'] = text
        #     redis_client.set(user['username'], json.dumps(this_entry_obj))

        #     return "user_enter_type"
        # 


        elif state == "user_enter_name":
            telebot_instance.sendMessage(chat_id=chat_id, text="On a scale from \n1 (It's a want, I can still be happy without it) to \n5 (My life can't function without it). \nHow would you classify your expense?",
                                         reply_to_message_id=msg_id, reply_markup=purchase_type_keyboard_markup)

            this_entry_obj = json.loads(redis_client.get(user['username']))
            this_entry_obj['description'] = text
            redis_client.set(user['username'], json.dumps(this_entry_obj))

            return "user_enter_type"

        elif state == "user_enter_type":
            this_entry_obj = json.loads(redis_client.get(user['username']))
            this_entry_obj['type'] = text
            redis_client.set(user['username'], json.dumps(this_entry_obj))

            telebot_instance.sendMessage(chat_id=chat_id,
                                         text=f"Confirm you entry?\nAmount - {this_entry_obj['amount']}\nCategory - {this_entry_obj['category']}\nDescription - {this_entry_obj['description']}\nPurchase Type - {this_entry_obj['type']} (are you sure?)\nExpense Time - {this_entry_obj['datetime']}",
                                         reply_to_message_id=msg_id, reply_markup=confirm_create_keyboard_markup)
            return "user_finish_input"

        elif state == "user_finish_input":
            this_entry_obj = json.loads(redis_client.get(user['username']))

            db_entry = ExpenseEntry()
            db_entry.username = this_entry_obj['username']
            db_entry.amount = this_entry_obj['amount']
            db_entry.category = this_entry_obj['category']
            db_entry.datetime = this_entry_obj['datetime']
            db_entry.description = this_entry_obj['description']
            db_entry.type = this_entry_obj['type']
            db_entry.submit_time = datetime.now().astimezone(singapore).strftime("%d/%m/%Y %H:%M:%S")
            entries = ExpenseEntry.query.filter(ExpenseEntry.username == username).order_by(ExpenseEntry.datetime.desc()).all()
            current_count = len(entries)

            action = UserAction()
            action.username = username
            action.chat_id = chat_id
            action.input = text
            action.datetime = datetime.now().astimezone(singapore).strftime("%d/%m/%Y %H:%M:%S")
            db.session.add(action)
            db.session.commit()

            try:
                db.session.add(db_entry)
                db.session.commit()
            except Exception as e:
                print(f"exception {e}")

            # target count here
            if current_count < 30:
                message = f"Creation success! \n\nWith {30 - current_count} more entries, we will be able to give you an overview of your spending habits!"
            else:
                message = f"Creation success! \nYou have logged in {current_count}, we will be analysing your latest 30 entries to generate an overview of your spending habits!"

            telebot_instance.sendMessage(chat_id=chat_id, text=message,
                                         reply_to_message_id=msg_id, reply_markup=start_keyboard_markup)

            redis_client.delete(user['username'] + "state")
            redis_client.delete(user['username'])
            return

        elif state == "user_enter_info_age":
            telebot_instance.sendMessage(chat_id=chat_id, text="Creation Success! Thank you for logging",
                                         reply_to_message_id=msg_id, reply_markup=info_input_keyboard_markup)
            return "user_enter_info_gender"

        elif state == "user_enter_info_gender":
            telebot_instance.sendMessage(chat_id=chat_id, text="Creation Success! Thank you for logging",
                                         reply_to_message_id=msg_id, reply_markup=info_input_keyboard_markup)
            return "user_enter_info_occupation"

        elif state == "user_enter_info_occupation":
            return

        elif state == "user_query_logs":
            if text == "list view":
                telebot_instance.sendMessage(chat_id=chat_id, text=f"Your expense list - {URL}view-data?username={username}",
                                    reply_to_message_id=msg_id, reply_markup=my_logs_keyboard_markup)
            elif text == "spending stats":
                return "user_query_stats"
            else:
                telebot_instance.sendMessage(chat_id=chat_id, text=f"View your expense here",
                    reply_to_message_id=msg_id, reply_markup=my_logs_keyboard_markup)
            return "user_query_logs"

    # no state
    else:
        if text == "/start" or text == "cancel delete" or text == "cancel create" or text == "back to home":
            telebot_instance.sendMessage(chat_id=chat_id, text="What would you like to do",
                                         reply_to_message_id=msg_id, reply_markup=start_keyboard_markup)
        elif text == "create expense":
            # 220 get most recent 5 spending
            entries = ExpenseEntry.query.filter(ExpenseEntry.username == username).order_by(ExpenseEntry.datetime.desc()).limit(3)
            
            telebot_instance.sendMessage(chat_id=chat_id,
                                         text="How much did you spend? \n\nyou can use /home to go back ",
                                         reply_to_message_id=msg_id, reply_markup=telegram.ReplyKeyboardRemove(remove_keyboard=True))
            return "user_enter_amount"
        elif text == "view my info":
            telebot_instance.sendMessage(chat_id=chat_id,
                                         text="Your details are ",
                                         reply_to_message_id=msg_id, reply_markup=info_keyboard_markup)
            return
        elif text == "enter my info":
            telebot_instance.sendMessage(chat_id=chat_id,
                                         text="You can view or edit your personal details",
                                         reply_to_message_id=msg_id, reply_markup=info_keyboard_markup)
            return "user_enter_info_age"
        elif text == "delete":
            telebot_instance.sendMessage(chat_id=chat_id, text="Delete the last entry?", reply_to_message_id=msg_id,
                                         reply_markup=delete_keyboard_markup)
        elif text == "my logs":

            action = UserAction()
            action.username = username
            action.chat_id = chat_id
            action.input = text
            action.datetime = datetime.now().astimezone(singapore).strftime("%d/%m/%Y %H:%M:%S")
            db.session.add(action)
            db.session.commit()

            telebot_instance.sendMessage(chat_id=chat_id,
                                         text=f"View your spending records here",
                                         reply_to_message_id=msg_id,
                                         reply_markup=my_logs_keyboard_markup)
            return "user_query_logs"
        else:
            telebot_instance.sendMessage(chat_id=chat_id, text="Whatchu wanna do, use /start to open up the menu",
                                         reply_to_message_id=msg_id,
                                         reply_markup=start_keyboard_markup)

    try:
        info = "got text message: " + text + " from " + user.username
        print(info)
    except:
        print("no message is received")
    return
