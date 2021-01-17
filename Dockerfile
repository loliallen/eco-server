FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apk update
RUN apk add --virtual gcc

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "app.ini"]