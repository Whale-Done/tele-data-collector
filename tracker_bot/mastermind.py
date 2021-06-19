from datetime import datetime, date
import json
import pytz

import telegram
import logging

from .model import ExpenseEntry, UserAction
from .credentials import DEPLOY_URL, DEBUG_URL
from appconfig import AppConfig
from .services import MasterMindService
from .keyboard import (
    start_keyboard_markup,
)

if AppConfig.debug:
    URL = DEBUG_URL
else:
    URL = DEPLOY_URL


def main_command_handler(incoming_message, telebot_instance, redis_client, db):
    """Echo the user message."""
    chat_id = incoming_message.chat.id
    msg_id = incoming_message.message_id
    user = incoming_message.from_user
    username = user["username"]

    text = incoming_message.text.encode("utf-8").decode()

    # check if current user has state
    if redis_client.get(user["username"] + "state") is not None:
        if (
            text == "cancel delete"
            or text == "cancel create"
            or text == "back to home"
            or text == "/home"
        ):
            redis_client.delete(user["username"] + "state")
            telebot_instance.sendMessage(
                chat_id=chat_id,
                text="What would you like to do",
                reply_to_message_id=msg_id,
                reply_markup=start_keyboard_markup,
            )
            return

        # step 1 of creating an expense entry
        state = redis_client.get(user["username"] + "state").decode("utf-8")
        if state == "user_enter_amount":
            return MasterMindService.handle_input_amount(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                user=user,
                telebot_instance=telebot_instance,
                redis_client=redis_client,
            )

        elif state == "user_enter_date":
            return MasterMindService.handle_input_date(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                user=user,
                telebot_instance=telebot_instance,
                redis_client=redis_client,
            )

        elif state == "user_enter_category":
            return MasterMindService.handle_input_category(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                user=user,
                telebot_instance=telebot_instance,
                redis_client=redis_client,
            )

        elif state == "user_enter_item_name":
            return MasterMindService.handle_input_item_name(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                user=user,
                telebot_instance=telebot_instance,
                redis_client=redis_client,
            )

        elif state == "user_enter_need_index":
            return MasterMindService.handle_input_need_index(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                user=user,
                telebot_instance=telebot_instance,
                redis_client=redis_client,
            )

        elif state == "user_finish_input":
            return MasterMindService.handle_input_finish(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                user=user,
                telebot_instance=telebot_instance,
                redis_client=redis_client,
                username=username,
                db=db,
            )

    # no state
    else:
        if (
            text == "/start"
            or text == "cancel delete"
            or text == "cancel create"
            or text == "back to home"
        ):
            telebot_instance.sendMessage(
                chat_id=chat_id,
                text="What would you like to do",
                reply_to_message_id=msg_id,
                reply_markup=start_keyboard_markup,
            )
        elif text == "create expense":
            entries = (
                ExpenseEntry.query.filter(ExpenseEntry.username == username)
                .order_by(ExpenseEntry.datetime.desc())
                .limit(3)
            )

            telebot_instance.sendMessage(
                chat_id=chat_id,
                text="How much did you spend? \n\nyou can use /home to go back ",
                reply_to_message_id=msg_id,
                reply_markup=telegram.ReplyKeyboardRemove(remove_keyboard=True),
            )
            return "user_enter_amount"

        elif text == "my spending diagnosis":
            return MasterMindService.user_query_diagnosis(
                text=text,
                chat_id=chat_id,
                msg_id=msg_id,
                username=username,
                telebot_instance=telebot_instance,
                db=db,
            )

        else:
            telebot_instance.sendMessage(
                chat_id=chat_id,
                text="Hello there! Thank you for using Whale 🐳 \n\nWhale is learning to help you understand your spending habits better\n\nuse /start to explore what Whale can do for you!",
                reply_to_message_id=msg_id,
                reply_markup=start_keyboard_markup,
            )
    return
