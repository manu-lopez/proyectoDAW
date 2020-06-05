# Pull from official image
FROM python:3.8-buster

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# Create and set work directory
RUN mkdir /code
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt /code/

RUN apt-get update
RUN pip install -r requirements.txt

# Copy project
COPY /proyecto /code/