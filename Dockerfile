FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev musl-dev
RUN apk update

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn","-b 0.0.0.0:5000","run:app"]