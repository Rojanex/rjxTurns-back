from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from app.routes.queue import queue_bp
from app.utils.manage_queue import *

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)
    queues_info = create_queues_from_json()    
    app.config['queues_info'] = queues_info  # Store queues_info in the app context
    app.register_blueprint(queue_bp, url_prefix='/queue')
    db.init_app(app)
    return app