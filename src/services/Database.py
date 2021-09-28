from mongoengine import connect

from src.config import Configuration


def global_connect():
    print("DB_URL", Configuration.DB_URL)
    try:
        params = {
            "alias": "core",
            "name": Configuration.DB_NAME,
            "host": Configuration.DB_URL,
            "serverSelectionTimeoutMS": Configuration.DB_TIMEOUT,
        }
        if not Configuration.DEBUG:
            params.update({
                "username": Configuration.DB_USERNAME,
                "password": Configuration.DB_PASSWORD,
            })
        db = connect(**params)
        print("[Database]: Connected")
    except ConnectionError:
        print("Error while connecting to Database")
