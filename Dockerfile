FROM python:3

# Avoid cache purge by adding requirements first
ADD ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt