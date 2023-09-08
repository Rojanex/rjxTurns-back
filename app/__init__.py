from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from .config import Config
from app.routes.queue import queue_bp
from app.routes.data import data_bp
from app.utils.manage_queue import *
from .extensions import db, socketio
from dotenv import load_dotenv
from app.utils.db_functions import connection_db, check_unfinished_elements 
import os
import urllib3


load_dotenv()

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins='*')
    config = Config()
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        conn = connection_db()
        folder_root = os.getcwd()
        queues_info = create_queues_from_json(conn=conn, filename=folder_root)    
        app.config['queues_info'] = queues_info  # Store queues_info in the app context
        app.config['folder_path'] = os.environ.get('FOLDER_PATH')

    with app.app_context():
        create_tables()
        check_unfinished_elements(conn)   

    app.config['total_modules'] = os.environ.get('NUM_MODULES')
    app.register_blueprint(queue_bp, url_prefix='/queue')
    app.register_blueprint(data_bp, url_prefix='/data')
    
    
    return app

def create_tables():
    db.create_all()
    print("Tables created if not exist.")