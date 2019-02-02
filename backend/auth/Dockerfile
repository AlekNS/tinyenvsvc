FROM python:3.6-alpine

RUN adduser -D auth
USER auth

WORKDIR /home/auth

COPY app .
COPY .env.prod .env
COPY requirements.txt .

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["/usr/bin/python3"]
