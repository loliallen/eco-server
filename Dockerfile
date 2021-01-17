FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN sudo apt update
RUN sudo apt install build-essential

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "app.ini"]