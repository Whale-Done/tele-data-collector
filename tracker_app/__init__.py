import os
import redis
from redis import Redis


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from appconfig import AppConfig
from tracker_app.config import DeployConfig, DebugConfig
from tracker_app.main.routes import main

app = Flask(__name__)

# for deploy
REDIS_DEFAULT_CONNECTION_POOL = redis.ConnectionPool.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/'))
redis_client = Redis(connection_pool=REDIS_DEFAULT_CONNECTION_POOL)

# for local debug
# redis_client = FlaskRedis(app)
db = SQLAlchemy(app)

# app.config.from_object(Config)
if AppConfig.debug:
    app.config.from_object(DebugConfig)
else:
    app.config.from_object(DeployConfig)

# import the routes as classes and register these blueprints into the flask app


app.register_blueprint(main)
