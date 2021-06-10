import os

from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from tracker_app.config import Config
from tracker_app.main.routes import main

app = Flask(__name__)
redis_client = FlaskRedis(app)
db = SQLAlchemy(app)

app.config.from_object(Config)

# import the routes as classes and register these blueprints into the flask app


app.register_blueprint(main)
