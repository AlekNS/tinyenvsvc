FROM python:3.6-alpine

RUN adduser -D auth

WORKDIR /home/auth

COPY .env.prod .env
COPY requirements.txt .

RUN apk add --update --no-cache gcc make libc-dev libffi-dev openssl-dev && \
    pip install jwt && \
    python -m venv venv && \
    venv/bin/pip install -r requirements.txt && \
    apk del gcc make

USER auth
COPY auth auth

EXPOSE 8080
ENTRYPOINT ["/home/auth/venv/bin/python3"]
CMD ["-m", "auth", "serve"]
