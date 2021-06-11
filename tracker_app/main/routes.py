from flask import Blueprint
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return "Home"


@main.route("/viewdata")
def view_data():
    return "DataPage"
