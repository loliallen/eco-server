from mongoengine import Document, StringField, IntField

from src.models.utils.BaseCrud import BaseCrud


class Test(Document, BaseCrud):
    test_name = StringField()
    coins_to_unlock = IntField()
    description = StringField()
    points_to_success = IntField()

    meta = {
        "db_alias": "core",
        "collection": "test"
    }
