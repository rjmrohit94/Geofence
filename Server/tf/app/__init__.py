import os
from pathlib import Path
from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect
from redis import Redis
import rq
from dotenv import dotenv_values

app = Flask(__name__)


base_path = Path(app.root_path).parent
# Configurations
app.config.from_pyfile(os.path.join(base_path, 'settings.py'))
config = dotenv_values(os.path.join(base_path, '.env'))
app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue(app.config['REDIS_JOB_QUEUE_NAME'], connection=app.redis)
mongo = MongoEngine(app)

connect(app.config['MONGODB_SETTINGS']['db'], alias=app.config['MONGODB_SETTINGS']['db'],
        host=app.config['MONGODB_SETTINGS']['host'], port=app.config['MONGODB_SETTINGS']['port'])
