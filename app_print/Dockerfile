# pull official base image
FROM python
# create working directory
ADD app.py .
RUN pip install requests python-dotenv python-socketio Pillow flask
RUN sudo apt-get install -y locale-all
# start app
CMD ["python", "./app.py"]