FROM python:3.9
LABEL maintainer "Howl Automation"
RUN mkdir /app
COPY requirements.txt .
COPY . .
RUN python -m pip install requirements2.txt
EXPOSE 5000
CMD ["python", "./run.py"]