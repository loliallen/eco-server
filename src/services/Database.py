from mongoengine import connect

from src.config import Configuration


def global_connect():
    print("DB_URL", Configuration.DB_URL)
    try:
        db = connect(
            alias="core",
            name="eco",
            host=Configuration.DB_URL,
            tlsCertificateKeyFile=Configuration.DB_SERT,
        )
        print("[Database]: Connected")
    except ConnectionError:
        print("Error while connecting to Database")
