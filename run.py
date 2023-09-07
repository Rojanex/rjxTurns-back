from gevent import monkey
monkey.patch_all()

import urllib3
urllib3.disable_warnings()

from app import create_app
import socket

app = create_app()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    app.run(debug=True, host=host)
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()