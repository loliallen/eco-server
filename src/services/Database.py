import os
from mongoengine import connect

DB_URL = os.getenv("DB_URL") 

if DB_URL == None:
    DB_URL = "mongodb://localhost:27017"

def global_connect():
    print("DB_URL", DB_URL)
    try:
        db = connect(
            alias="core",
            name="eco",
            host=DB_URL
        )
        print("[Database]: Connected")
    except ConnectionError:
        print("Error while connecting to Database")