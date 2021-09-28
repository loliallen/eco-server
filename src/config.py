import datetime
import os
import pathlib

from src.utils.custom_swagger import JSONEncoder


class Configuration:
    BABEL_DEFAULT_LOCALE = 'ru'

    SECRET_KEY = 'a really really really really long secret key'  # TODO вынести в секреты
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_ADMIN_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_TOKEN_LOCATION = 'headers'
    PROPAGATE_EXCEPTIONS = True

    RECOVERY_TOKEN_EXPIRES = datetime.timedelta(seconds=120)

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cronenbergclaw@gmail.com'  # введите свой адрес электронной почты здесь
    MAIL_DEFAULT_SENDER = 'cronenbergclaw@gmail.com'  # и здесь
    MAIL_PASSWORD = 'eikbzcpodtroenca'  # TODO вынести в секреты

    PASSWORD_HASH_FUNC = 'sha256'  # алгоритм генерации пароля, если поменять все текущие пароли слетят
    PASSWORD_GENERATE_ITERATIONS = 10000  # кол-во итераций при генерации пароля, если поменять все текущие пароли слетят

    DB_NAME = os.getenv("MONGO_INITDB_DATABASE", default="eco")
    DB_URL = os.getenv("DB_URL", default=f"mongodb://0.0.0.0:27017")
    DB_USERNAME = os.getenv("MONGO_USERNAME", default="user")
    DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="password")
    DB_SERT = os.getenv("DB_SERT", default='mongo.pem')
    DB_TIMEOUT = os.getenv("DB_TIMEOUT", default=5000)

    HOST = os.getenv("HOST", default="0.0.0.0")
    PORT = os.getenv("PORT", default=8000)

    DEBUG = os.getenv("DEBUG", 'True') == 'True'
    PROTOCOL = "http" if DEBUG else "https"

    USER_SWAGGER_URL = '/api/docs'
    USER_SCHEMA_URL = f'{PROTOCOL}://{HOST}:{PORT}/api/doc/swagger.json'

    ADMIN_SWAGGER_URL = '/api/docs'
    ADMIN_SCHEMA_URL = f'{PROTOCOL}://{HOST}:8000/api/doc/swagger.json'

    ECO_COINS_BY_INVITE = 15
    ECO_COINS_BY_OFFER_NEW_REC_POINT = 30
    ECO_COINS_BY_OFFER_CHANGE_REC_POINT = 20

    WEIGHT_RECYCLE_TO_NEED_APPROVE = 10
    TEST_FREEZE_TIME = datetime.timedelta(days=1)
    MAX_RADIUS_REC_POINTS_SHOW = 100

    STATIC_FOLDER = os.getenv("STATIC_FOLDER", str(pathlib.Path(__file__).parent.absolute() / "statics"))
    STATIC_URL_PATH = '/statics'

    STATIC_URL = f"{PROTOCOL}://{HOST}:{PORT}{STATIC_URL_PATH}/"
    if not os.path.exists(STATIC_FOLDER):
        os.mkdir(STATIC_FOLDER)

    RESTFUL_JSON = {'cls': JSONEncoder}
