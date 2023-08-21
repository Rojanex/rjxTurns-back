from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import Config
from app.routes.queue import queue_bp
from app.utils.manage_queue import *
from .extensions import db
from dotenv import load_dotenv
import os

load_dotenv()

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)
    
    queues_info = create_queues_from_json()    
    app.config['queues_info'] = queues_info  # Store queues_info in the app context
    app.config['total_modules'] = os.environ.get('NUM_MODULES')
    app.register_blueprint(queue_bp, url_prefix='/queue')
    db.init_app(app)
    ma.init_app(app)
    from app.models.models import FilaMaestra
    with app.app_context():
        create_tables()      
    return app

def create_tables():
    db.create_all()
    print("Tables created if not exist.")