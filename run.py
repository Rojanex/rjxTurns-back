from gevent import monkey
monkey.patch_all()

import urllib3
urllib3.disable_warnings()

from app import create_app
from flask_socketio import SocketIO

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="192.168.7.38")
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()