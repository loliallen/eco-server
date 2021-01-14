FROM python:3.7-alpine

COPY . /app

WORKDIR /app 

RUN python -m venv env
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "src/app.py"]