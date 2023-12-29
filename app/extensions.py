from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import logging

db = SQLAlchemy()
socketio = SocketIO(async_mode='gevent')


logger = logging.getLogger('app')
logger.setLevel(logging.WARNING) # will handle all messages that have a severity level of WARNING or higher (i.e., ERROR, CRITICAL). 
handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
