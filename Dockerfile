FROM python:3.9
LABEL maintainer "Howl Automation"
RUN mkdir /app
COPY requirements.txt .
COPY . .
RUN pyhton -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./run.py"]