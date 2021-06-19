from telegram import KeyboardButton, ReplyKeyboardMarkup

start_keyboard_buttons = [
    [KeyboardButton("create expense")],
    [KeyboardButton("my spending diagnosis")],
]
start_keyboard_markup = ReplyKeyboardMarkup(start_keyboard_buttons)

info_keyboard_buttons = [
    [KeyboardButton("view my info")],
    [KeyboardButton("enter my info")],
    [KeyboardButton("home")],
]
info_keyboard_markup = ReplyKeyboardMarkup(info_keyboard_buttons)

info_input_keyboard_buttons = [[KeyboardButton("skips")], [KeyboardButton("home")]]
info_input_keyboard_markup = ReplyKeyboardMarkup(info_input_keyboard_buttons)

delete_keyboard_buttons = [
    [KeyboardButton("confirm delete")],
    [KeyboardButton("cancel delete")],
]
delete_keyboard_markup = ReplyKeyboardMarkup(delete_keyboard_buttons)

amount_keyboard_buttons = [
    [KeyboardButton("less than 1")],
    [KeyboardButton("around 5")],
    [KeyboardButton("cancel create")],
]
amount_keyboard_markup = ReplyKeyboardMarkup(amount_keyboard_buttons)

category_keyboard_buttons = [
    [KeyboardButton("food"), KeyboardButton("drinks")],
    [KeyboardButton("snacks"), KeyboardButton("transportation")],
    [KeyboardButton("hobbies"), KeyboardButton("subscription/top up")],
    [KeyboardButton("cancel create")],
]
category_keyboard_markup = ReplyKeyboardMarkup(category_keyboard_buttons)

date_keyboard_buttons = [
    [KeyboardButton("Now (Or recent)"), KeyboardButton("Today morning")],
    [KeyboardButton("Today noon"), KeyboardButton("Today evening")],
    [KeyboardButton("cancel create")],
]
date_keyboard_markup = ReplyKeyboardMarkup(date_keyboard_buttons)

item_name_keyboard_buttons = [
    [KeyboardButton("None (Leave blank)")],
    [KeyboardButton("cancel create")],
]
item_name_keyboard_markup = ReplyKeyboardMarkup(item_name_keyboard_buttons)

purchase_type_keyboard_buttons = [
    [KeyboardButton("1 (Pure Want)"), KeyboardButton("2")],
    [KeyboardButton("3"), KeyboardButton("4")],
    [KeyboardButton("5 (Real need!)"), KeyboardButton("cancel create")],
]
purchase_type_keyboard_markup = ReplyKeyboardMarkup(purchase_type_keyboard_buttons)

confirm_create_keyboard_buttons = [
    [KeyboardButton("confirm create")],
    [KeyboardButton("cancel create")],
]
confirm_create_keyboard_markup = ReplyKeyboardMarkup(confirm_create_keyboard_buttons)

my_logs_keyboard_buttons = [
    [KeyboardButton("list view")],
    [KeyboardButton("spending stats")],
    [KeyboardButton("back to home")],
]
my_logs_keyboard_markup = ReplyKeyboardMarkup(my_logs_keyboard_buttons)
