import os
import redis
from redis import Redis


from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from tracker_app.config import Config
from tracker_app.main.routes import main

app = Flask(__name__)

# for deploy
# redis_client = Redis(host="ec2-54-221-249-45.compute-1.amazonaws.com", port=14060, db=0, password='p22272393a04e83e3c4b7cbe21faa98ac3d93cf57e55203ffa43eef0f3a2d5113', ssl=True)
REDIS_DEFAULT_CONNECTION_POOL = redis.ConnectionPool.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/'))
redis_client = Redis(connection_pool=REDIS_DEFAULT_CONNECTION_POOL)

# for local debug
# redis_client = FlaskRedis(app)
db = SQLAlchemy(app)

app.config.from_object(Config)

# import the routes as classes and register these blueprints into the flask app


app.register_blueprint(main)
