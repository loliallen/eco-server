FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

RUN pip install --no-chache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "src/app.py"]