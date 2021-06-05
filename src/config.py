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

    DB_NAME = "eco"
    DB_PASSWORD = "eCo1251kek"  # TODO при выходе в прод вынести
    DB_URL = os.getenv("DB_URL", default=f"mongodb+srv://root:{DB_PASSWORD}@eco.y8cj7.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
    HOST = os.getenv("HOST", default="0.0.0.0")

    USER_SWAGGER_URL = '/api/docs'
    USER_SCHEMA_URL = f'https://{HOST}:5000/api/doc/swagger.json'

    ADMIN_SWAGGER_URL = '/api/docs'
    ADMIN_SCHEMA_URL = f'https://{HOST}:8000/api/doc/swagger.json'

    ECO_COINS_BY_INVITE = 15
