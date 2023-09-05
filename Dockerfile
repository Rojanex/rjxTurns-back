FROM python:3.9
LABEL maintainer "Howl Automation"
RUN pip install --upgrade pip
RUN mkdir /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./run.py"]