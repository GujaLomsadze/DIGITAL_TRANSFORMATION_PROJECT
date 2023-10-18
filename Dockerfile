# Dockerfile

# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .