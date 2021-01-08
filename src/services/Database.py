from mongoengine import connect


def global_connect():
    db = connect(
        alias="core",
        name="eco",
        # username="",
        # password="",
        host="localhost:27017"
    )
    print("[Database]: Connected")