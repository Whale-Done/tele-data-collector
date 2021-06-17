from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
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


class UserAction(db.Model):
    __tablename__ = "user_actions"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    chat_id = db.Column(db.String(128))
    input = db.Column(db.String(128))