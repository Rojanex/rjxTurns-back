from app import create_app
from gevent.pywsgi import WSGIServer
from flask_socketio import SocketIO

from gevent import monkey

monkey.patch_all()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="192.168.7.38")
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()