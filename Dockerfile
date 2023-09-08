FROM python:3.9
LABEL maintainer "Howl Automation"
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
COPY run.py run.py
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]