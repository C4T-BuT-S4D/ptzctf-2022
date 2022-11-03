FROM python:3.9.6-slim-bullseye

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app .

CMD gunicorn app:app --bind 0.0.0.0:5321 --workers 3
