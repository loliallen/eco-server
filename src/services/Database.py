import os
from mongoengine import connect

DB_URL = os.getenv("DB_URL")

def global_connect():
    db = connect(
        alias="core",
        name="eco",
        host=DB_URL
    )
    print("[Database]: Connected")