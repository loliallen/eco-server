from mongoengine import connect

from src.config import Configuration


def global_connect(logger):
    logger.info(f"DB_URL {Configuration.DB_URL}")
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
    try:
        connect(**params)
    except ConnectionError:
        logger.error("Error while connecting to Database")
        raise
    else:
        logger.info("[Database]: Connected")
