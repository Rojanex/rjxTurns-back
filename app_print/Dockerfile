# pull official base image
FROM python
# create working directory
ADD app.py .
RUN apt-get update && \
    apt-get install -y locales-all && \
    pip install requests python-dotenv python-socketio Pillow flask
# start app
EXPOSE 5001
CMD ["python", "./app.py"]
#docker run --env-file ./.env your_image_name