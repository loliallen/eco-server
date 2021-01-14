FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5000

ENTRYPOINT ["python3", "src/app.py"]