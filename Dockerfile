FROM python:3.12-slim-bookworm AS builder

RUN apt-get update

RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  gcc \
  && apt-get clean \


RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM python:3.12-slim-bookworm as app

ENV PYTHONUNBUFFERED True

COPY --from=builder / /

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

EXPOSE $PORT

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 4 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 server.wsgi