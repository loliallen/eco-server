import datetime
import os
import pathlib


class Configuration:
    SECRET_KEY = 'a really really really really long secret key'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_TOKEN_LOCATION = 'headers'
    PROPAGATE_EXCEPTIONS = True

    RECOVERY_TOKEN_EXPIRES = datetime.timedelta(seconds=120)

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
    PORT = os.getenv("PORT", default=8000)

    DEBUG = os.getenv("DEBUG", 'True') == 'True'
    PROTOCOL = "http" if DEBUG else "https"

    USER_SWAGGER_URL = '/api/docs'
    USER_SCHEMA_URL = f'{PROTOCOL}://{HOST}:{PORT}/api/doc/swagger.json'

    ADMIN_SWAGGER_URL = '/api/docs'
    ADMIN_SCHEMA_URL = f'{PROTOCOL}://{HOST}:8000/api/doc/swagger.json'

    ECO_COINS_BY_INVITE = 15
    WEIGHT_RECYCLE_TO_NEED_APPROVE = 10
    TEST_FREEZE_TIME = datetime.timedelta(days=15)

    STATIC_FOLDER = os.getenv("STATIC_FOLDER", str(pathlib.Path(__file__).parent.absolute() / "statics"))
    STATIC_URL_PATH = '/statics'

    STATIC_URL = f"{PROTOCOL}://{HOST}:{PORT}{STATIC_URL_PATH}/"
    if not os.path.exists(STATIC_FOLDER):
        os.mkdir(STATIC_FOLDER)
