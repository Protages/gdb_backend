# Builder
FROM python:3.10.5-slim as builder

WORKDIR /core/app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /core/app/src/wheels -r requirements.txt

COPY ./src .


# FINAL
FROM python:3.10.5-slim

# create directory for the app user
RUN mkdir -p /home/app

# create group - app, user - app
RUN addgroup --system app && adduser --system app && adduser app app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update
COPY --from=builder /core/app/src/wheels /wheels
COPY --from=builder /core/app/src/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
