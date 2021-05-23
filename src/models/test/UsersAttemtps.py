from mongoengine import Document, StringField, IntField, ReferenceField, BooleanField

from src.models.test.Test import Test
from src.models.user.UserModel import User
from src.models.utils.BaseCrud import BaseCrud


class UserAttempts(Document, BaseCrud):
    user = ReferenceField(User, required=True)
    test = ReferenceField(Test, required=True)
    points = IntField()
    is_success = BooleanField(required=True, default=False)

    meta = {
        "db_alias": "core",
        "collection": "user_attempts"
    }
