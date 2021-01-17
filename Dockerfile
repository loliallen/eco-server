FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["gunicorn","-b", "0.0.0.0:5000", "./src/wsgi:app"]