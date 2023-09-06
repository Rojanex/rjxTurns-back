FROM python:3.9
LABEL maintainer "Howl Automation"
RUN mkdir /app
COPY requirements.txt .
COPY . .
RUN python -m pip install \
    requests \
    python-dotenv python-socketio Pillow flask \
    flask_marshmallow flask_sqlalchemy flask_socketio \
    psycopg2 Pillow urllib2 gevent  marshmallow-sqlalchemy
EXPOSE 5000
CMD ["python", "./run.py"]