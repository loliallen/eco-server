from mongoengine import Document, StringField, IntField, BooleanField

from src.models.utils.BaseCrud import BaseCrud


class Test(Document, BaseCrud):
    test_name = StringField()
    coins_to_unlock = IntField()
    description = StringField()
    points_to_success = IntField()
    is_active = BooleanField(default=False)

    meta = {
        "db_alias": "core",
        "collection": "test",
        "strict": False
    }
