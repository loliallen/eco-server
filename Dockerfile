FROM python:3.7-alpine

ENV http_proxy http://proxy-chain.xxx.com:911/
ENV https_proxy http://proxy-chain.xxx.com:912/

COPY . /app

WORKDIR /app 

RUN python -m venv env
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "src/app.py"]