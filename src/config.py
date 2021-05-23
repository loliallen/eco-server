import datetime
import os


class Configuration:
    SECRET_KEY = 'a really really really really long secret key'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_TOKEN_LOCATION = 'headers'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cronenbergclaw@gmail.com'  # введите свой адрес электронной почты здесь
    MAIL_DEFAULT_SENDER = 'cronenbergclaw@gmail.com'  # и здесь
    MAIL_PASSWORD = 'eikbzcpodtroenca'

    DB_URL = os.getenv("DB_URL", default="mongodb://localhost:27017")
    HOST = os.getenv("HOST", default="0.0.0.0")

    USER_SWAGGER_URL = '/api/docs'
    USER_SCHEMA_URL = f'http://{HOST}:5000/api/doc/swagger.json'

    ADMIN_SWAGGER_URL = '/api/docs'
    ADMIN_SCHEMA_URL = f'http://{HOST}:8000/api/doc/swagger.json'
