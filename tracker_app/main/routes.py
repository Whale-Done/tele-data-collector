from flask import Blueprint, render_template, request, make_response

main = Blueprint('main', __name__)
from ..model import ExpenseEntry, db


@main.route("/")
@main.route("/home")
def home():
    return "Home"


@main.route("/view-data", methods=['GET'])
def view_data():
    try:
        username = request.args.get('username')
    except KeyError:
        return make_response('Username Error', 404)

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
    return render_template('dataview.html', expense_detail_list=expense_detail_list)

@main.route("/view-data-test", methods=['GET'])
def view_data_test():
    expense_detail_list = [{
        'amount': '1',
        'category': 'test',
        'description': 'test',
        'purchase_type': 'test',
        'submit_time': 'test',
        'expense_time': 'test',
    }]
    return render_template('dataview.html', expense_detail_list=expense_detail_list)
