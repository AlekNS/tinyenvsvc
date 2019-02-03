FROM python:3.6-alpine

RUN adduser -D stats
USER stats

WORKDIR /home/stats

COPY app .
COPY requirements.txt .

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["/usr/bin/python3"]
CMD ["serve"]
