FROM python:3.9
LABEL maintainer "Howl Automation"
RUN mkdir /app
WORKDIR /app
COPY run.py /app
COPY .env /app
COPY app /app/app
COPY requirements.txt requirements.txt
RUN apt-get update  && apt-get install -y cups-client
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]