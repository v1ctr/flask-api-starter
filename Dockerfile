FROM python:3.7-alpine

ENV FLASK_APP run.py
ENV FLASK_CONFIG docker

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN adduser -D appuser
USER appuser

WORKDIR /home/appuser

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY run.py config.py boot.sh ./

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]