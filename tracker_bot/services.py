import json
from datetime import datetime, date
import pytz

from telegram import ReplyKeyboardRemove, user

from .model import UserAction, ExpenseEntry
from .keyboard import (
    date_keyboard_markup,
    category_keyboard_markup,
    confirm_create_keyboard_markup,
    purchase_type_keyboard_markup,
    start_keyboard_markup,
)

singapore = pytz.timezone("Asia/Singapore")
gmt = pytz.timezone("Etc/GMT")
kuala_lumpur = pytz.timezone("Asia/Kuala_Lumpur")


class MasterMindService:
    def handle_input_amount(
        text, chat_id, msg_id, user, telebot_instance, redis_client
    ):
        valid_input = True
        try:
            if "$" in text:
                text = text.replace("$", "")
            float(text)
        except:
            valid_input = False

        if valid_input:
            current_data_string = json.dumps(
                {"username": user["username"], "amount": text}
            )

            telebot_instance.sendMessage(
                chat_id=chat_id,
                text="When did you make this expense",
                reply_to_message_id=msg_id,
                reply_markup=date_keyboard_markup,
            )
            redis_client.set(user["username"], current_data_string)

            return "user_enter_date"

        else:
            telebot_instance.sendMessage(
                chat_id=chat_id,
                text="Please enter a valid amount, like 0.31, 2.7, 150\n\nUse /home to cancel and go back to home menu 🚫",
                reply_to_message_id=msg_id,
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
            )

            return "user_enter_amount"

    def handle_input_date(text, chat_id, msg_id, user, telebot_instance, redis_client):
        telebot_instance.sendMessage(
            chat_id=chat_id,
            text="enter the category of your expense",
            reply_to_message_id=msg_id,
            reply_markup=category_keyboard_markup,
        )
        this_entry_obj = json.loads(redis_client.get(user["username"]))
        now = datetime.now()
        if text == "Now (Or recent)":
            dt_string = now.astimezone(singapore).strftime("%Y-%m-%d %H:%M:%S")
        elif text == "Today morning":
            today_morning = datetime(now.year, now.month, now.day, 9, 0, 0)
            dt_string = today_morning.strftime("%Y-%m-%d %H:%M:%S")
        elif text == "Today noon":
            today_noon = datetime(now.year, now.month, now.day, 12, 0, 0)
            dt_string = today_noon.strftime("%Y-%m-%d %H:%M:%S")
        elif text == "Today evening":
            today_evening = datetime(now.year, now.month, now.day, 21, 0, 0)
            dt_string = today_evening.strftime("%Y-%m-%d %H:%M:%S")
        else:
            dt_string = text

        this_entry_obj["datetime"] = dt_string
        redis_client.set(user["username"], json.dumps(this_entry_obj))

        return "user_enter_category"

    def handle_input_category(
        text, chat_id, msg_id, user, telebot_instance, redis_client
    ):
        telebot_instance.sendMessage(
            chat_id=chat_id,
            text="What item/service did you purchase? \n\nUse /home to go back",
            reply_to_message_id=msg_id,
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        this_entry_obj = json.loads(redis_client.get(user["username"]))
        this_entry_obj["category"] = text
        redis_client.set(user["username"], json.dumps(this_entry_obj))
        return "user_enter_item_name"

    def handle_input_need_index(
        text, chat_id, msg_id, user, telebot_instance, redis_client
    ):
        this_entry_obj = json.loads(redis_client.get(user["username"]))
        if text == "1 (Pure Want)":
            this_entry_obj["type"] = 1
        elif text == "2":
            this_entry_obj["type"] = 2
        elif text == "3":
            this_entry_obj["type"] = 3
        elif text == "4":
            this_entry_obj["type"] = 4
        elif text == "5 (Real need!)":
            this_entry_obj["type"] = 5
        else:
            telebot_instance.sendMessage(
                chat_id=chat_id,
                text=f"Please select an index within the given range using the keyboard below \n\n1 - pure want😍\n2 - kinda want it🤤\n3 - hesitation...🤥\n4 - kinda need it🤔\n5 - Legit need to spend for this 🤯",
                reply_to_message_id=msg_id,
                reply_markup=purchase_type_keyboard_markup,
            )
            return "user_enter_need_index"

        redis_client.set(user["username"], json.dumps(this_entry_obj))
        telebot_instance.sendMessage(
            chat_id=chat_id,
            text=f"Double check your log:\n\n💰 Amount - {this_entry_obj['amount']}\n🎲 Category - {this_entry_obj['category']}\n💬 Description - {this_entry_obj['description']}\n🔢 Need index - {this_entry_obj['type']}\n⏰ Expense Time - {this_entry_obj['datetime']}",
            reply_to_message_id=msg_id,
            reply_markup=confirm_create_keyboard_markup,
        )
        return "user_finish_input"

    def handle_input_item_name(
        text, chat_id, msg_id, user, telebot_instance, redis_client
    ):
        telebot_instance.sendMessage(
            chat_id=chat_id,
            text="How would you classify your expense using the following scale?\n\n1 - pure want😍\n2 - kinda want it🤤\n3 - hesitation...🤥\n4 - kinda need it🤔\n5 - legit need to spend for this 🤯 ",
            reply_to_message_id=msg_id,
            reply_markup=purchase_type_keyboard_markup,
        )

        this_entry_obj = json.loads(redis_client.get(user["username"]))
        this_entry_obj["description"] = text
        redis_client.set(user["username"], json.dumps(this_entry_obj))
        return "user_enter_need_index"

    def handle_input_finish(
        text, chat_id, msg_id, user, telebot_instance, redis_client, db, username
    ):
        this_entry_obj = json.loads(redis_client.get(user["username"]))

        db_entry = ExpenseEntry()
        db_entry.username = this_entry_obj["username"]
        db_entry.amount = this_entry_obj["amount"]
        db_entry.category = this_entry_obj["category"]
        db_entry.datetime = this_entry_obj["datetime"]
        db_entry.description = this_entry_obj["description"]
        db_entry.type = this_entry_obj["type"]
        db_entry.submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entries = (
            ExpenseEntry.query.filter(ExpenseEntry.username == username)
            .order_by(ExpenseEntry.datetime.desc())
            .all()
        )
        current_count = len(entries)

        action = UserAction()
        action.username = username
        action.chat_id = chat_id
        action.input = text
        action.datetime = date.today().strftime("%d/%m/%Y")
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

        telebot_instance.sendMessage(
            chat_id=chat_id,
            text=message,
            reply_to_message_id=msg_id,
            reply_markup=start_keyboard_markup,
        )

        redis_client.delete(user["username"] + "state")
        redis_client.delete(user["username"])
        return

    def get_weighted_need_score():
        return 1

    def user_query_diagnosis(text, chat_id, msg_id, telebot_instance, db, username, webhook_url):
        action = UserAction()
        action.username = username
        action.chat_id = chat_id
        action.input = text
        action.datetime = date.today().strftime("%d/%m/%Y")
        db.session.add(action)
        db.session.commit()

        rs = db.engine.execute(
            f"""
            SELECT COUNT(*) as count, type FROM entries
            WHERE
                username='{username}'
            GROUP BY
                type
            """
        )

        replyList = ""

        # Diagnostic feature
        TARGET_COUNT = 30
        entries = (
            ExpenseEntry.query.filter(ExpenseEntry.username == username)
            .order_by(ExpenseEntry.datetime.desc())
            .all()
        )
        current_count = len(entries)

        temp = sorted(
            [{"type": entry.type, "count": entry.count} for entry in rs],
            key=lambda k: k["type"],
        )

        for entry in temp:
            if entry["type"] == "1":
                replyList += (
                    f"""{entry["type"]} (pure want😍) count: *{entry["count"]}*\n"""
                )
            if entry["type"] == "2":
                replyList += (
                    f"""{entry["type"]} (kinda want it🤤) count: *{entry["count"]}*\n"""
                )
            if entry["type"] == "3":
                replyList += (
                    f"""{entry["type"]} (hesitation...🤥) count: *{entry["count"]}*\n"""
                )
            if entry["type"] == "4":
                replyList += (
                    f"""{entry["type"]} (kinda need it🤔) count: *{entry["count"]}*\n"""
                )
            if entry["type"] == "5":
                replyList += f"""{entry["type"]} (legit need to spend for this 🤯) count: *{entry["count"]}*\n"""

        expense_detail_list = [
            {
                "amount": entry.amount,
                "category": entry.category,
                "description": entry.description,
                "purchase_type": entry.type,
                "submit_time": entry.submit_time,
                "expense_time": entry.datetime,
            }
            for entry in entries
        ]

        aggregate_sum = 0
        amount_sum = 0
        for expense in expense_detail_list:
            product = int(expense["purchase_type"]) * float(expense["amount"])
            aggregate_sum += product
            amount_sum += float(expense["amount"])

        if len(expense_detail_list) > 0:
            replyList += f"""\n Your average Want Need Score is \n⭐️ {"%.2f" % round(aggregate_sum/amount_sum, 2)} ⭐️"""
            replyList += f"""\n\n 📝 View your expense list here \n {webhook_url}view-data?username={username}"""

        # replyList += f"""\n\n🚧 Whale is working on the following 🚧\nThe population average need index\nYour current percentile \nand many more! """

        # if target count not met, send this
        if current_count <= TARGET_COUNT:
            required_count = TARGET_COUNT - current_count

            telebot_instance.sendMessage(
                chat_id=chat_id,
                text=f"Let's see... \n\nwe still need {required_count} more entries to give you a more accurate report. \n\n{replyList}",
                reply_to_message_id=msg_id,
                reply_markup=start_keyboard_markup,
                parse_mode="Markdown",
            )
        else:
            # target count is met, send a more detailed report
            telebot_instance.sendMessage(
                chat_id=chat_id,
                text=f"Your stats -\n{replyList}",
                reply_to_message_id=msg_id,
                reply_markup=start_keyboard_markup,
            )
        return
