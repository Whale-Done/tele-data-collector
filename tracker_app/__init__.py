import os

from flask import Flask
from tracker_app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # import the routes as classes and register these blueprints into the flask app
    from tracker_app.main.routes import main

    app.register_blueprint(main)

    return app