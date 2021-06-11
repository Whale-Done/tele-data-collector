from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return "Home"


@main.route("/viewdata")
def view_data():
    amount_list = [4.5, 23, 3, 4, 5]
    expense_detail_list = [
        {
            'category': 'food',
            'description': 'lunch',
            'purchase_type': 'impulsive, but need?',
            'expense_time': '2021-06-12 12:00:31',
            'submit_time': '2021-06-12 12:30:00'
        },

        {
            'category': 'food',
            'description': 'lunch',
            'purchase_type': 'impulsive, but need?',
            'expense_time': '2021-06-12 12:00:31',
            'submit_time': '2021-06-12 12:30:00'
        },

        {
            'category': 'food',
            'description': 'lunch',
            'purchase_type': 'impulsive, but need?',
            'expense_time': '2021-06-12 12:00:31',
            'submit_time': '2021-06-12 12:30:00'
        },

        {
            'category': 'food',
            'description': 'lunch',
            'purchase_type': 'impulsive, but need?',
            'expense_time': '2021-06-12 12:00:31',
            'submit_time': '2021-06-12 12:30:00'
        },

        {
            'category': 'food',
            'description': 'lunch',
            'purchase_type': 'impulsive, but need?',
            'expense_time': '2021-06-12 12:00:31',
            'submit_time': '2021-06-12 12:30:00'
        },
    ]
    return render_template('dataview.html', amount_list=amount_list, expense_detail_list=expense_detail_list)
