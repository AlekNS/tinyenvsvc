FROM python:3.6-alpine

RUN adduser -D stats

WORKDIR /home/stats

COPY stats .
COPY requirements.txt .

RUN apk add --update --no-cache gcc make libc-dev libffi-dev openssl-dev && \
    pip install jwt && \
    python -m venv venv && \
    venv/bin/pip install -r requirements.txt && \
    apk del gcc make

USER stats
COPY stats stats

EXPOSE 8080
ENTRYPOINT ["/home/stats/venv/bin/python3"]
CMD ["-m", "stats", "serve"]
