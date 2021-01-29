import os
from mongoengine import connect

DB_URL = os.getenv("DB_URL") 

def global_connect():
    print(DB_URL)
    try:
        db = connect(
            alias="core",
            name="eco",
            host=DB_URL
        )
        print("[Database]: Connected")
    except:
        print("Error while connecting to Database")