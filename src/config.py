import datetime
import os
import pathlib

from src.utils.custom_swagger import JSONEncoder


class Configuration:
    BABEL_DEFAULT_LOCALE = 'ru'

    SECRET_KEY = os.getenv("SECRET_KEY", 'aa2258c1-4dd8-43dd-937a-9cd27ee774f0')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=os.getenv("JWT_ACCESS_TOKEN_EXPIRES", default=2))
    JWT_ADMIN_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=os.getenv("JWT_ADMIN_ACCESS_TOKEN_EXPIRES", default=2))
    JWT_TOKEN_LOCATION = 'headers'
    PROPAGATE_EXCEPTIONS = True

    RECOVERY_TOKEN_EXPIRES = datetime.timedelta(seconds=os.getenv("RECOVERY_TOKEN_EXPIRES", default=120))

    MAIL_SERVER = os.getenv("MAIL_SERVER", default='smtp.googlemail.com')
    MAIL_PORT = os.getenv("MAIL_PORT", default=587)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", default='True') == 'True'
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

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
    URL_ROOT_END = f":{PORT}" if PORT else ""

    DEBUG = os.getenv("DEBUG", default='True') == 'True'
    PROTOCOL = os.getenv("PROTOCOL", default="http" if DEBUG else "https")

    SWAGGER_URL = '/api/docs'
    SCHEMA_URL = f'{PROTOCOL}://{HOST}{URL_ROOT_END}/api/doc/swagger.json'

    ECO_COINS_BY_INVITE = os.getenv("ECO_COINS_BY_INVITE", default=15)
    ECO_COINS_BY_OFFER_NEW_REC_POINT = os.getenv("ECO_COINS_BY_OFFER_NEW_REC_POINT", default=30)
    ECO_COINS_BY_OFFER_CHANGE_REC_POINT = os.getenv("ECO_COINS_BY_OFFER_CHANGE_REC_POINT", default=20)

    WEIGHT_RECYCLE_TO_NEED_APPROVE = os.getenv("WEIGHT_RECYCLE_TO_NEED_APPROVE", default=15)
    TEST_FREEZE_TIME = datetime.timedelta(days=os.getenv("TEST_FREEZE_TIME", default=1))
    MAX_RADIUS_REC_POINTS_SHOW = os.getenv("MAX_RADIUS_REC_POINTS_SHOW", default=100)

    STATIC_FOLDER = os.getenv("STATIC_FOLDER", str(pathlib.Path(__file__).parent.absolute() / "statics"))
    STATIC_URL_PATH = '/statics'

    STATIC_URL = f'{PROTOCOL}://{HOST}:{URL_ROOT_END}{STATIC_URL_PATH}/'
    if not os.path.exists(STATIC_FOLDER):
        os.mkdir(STATIC_FOLDER)

    RESTFUL_JSON = {'cls': JSONEncoder}
