from mongoengine import Document, StringField, IntField, ReferenceField, BooleanField, ListField, DateTimeField

from src.models.test.Test import Test
from src.models.user.UserModel import User
from src.models.utils.BaseCrud import BaseCrud


class UserAttempts(Document, BaseCrud):
    user = ReferenceField(User, required=True)
    test = ReferenceField(Test, required=True)
    points = IntField(default=0)
    already_answered = ListField(ReferenceField('Question'))
    is_closed = BooleanField(required=True, default=False)
    is_success = BooleanField(required=True, default=False)
    datetime_opened = DateTimeField()
    datetime_closed = DateTimeField()

    meta = {
        "db_alias": "core",
        "collection": "user_attempts",
        "strict": False
    }
