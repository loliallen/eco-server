FROM python:3.7-alpine

COPY . /app

WORKDIR /app 

RUN python -m venv env
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python", "src/app.py"]