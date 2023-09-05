FROM python:3.6
LABEL maintainer "Howl Automation"
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000