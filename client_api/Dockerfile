FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /app/client_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .