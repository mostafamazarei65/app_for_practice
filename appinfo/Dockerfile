# Use an official Python runtime as a parent image
FROM python:alpine

WORKDIR /opt/app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
