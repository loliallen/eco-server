from mongoengine import connect


def global_connect():
    db = connect(
        alias="core",
        name="eco",
        username="user",
        password="pwd",
        host="localhost:27017"
    )
    print("[Database]: Connected")