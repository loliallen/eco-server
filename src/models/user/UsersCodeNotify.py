from datetime import datetime

from flask_login import UserMixin
from mongoengine import Document, StringField, DateTimeField, ReferenceField

from src.models.utils.Atomic import Atomic
from src.models.utils.BaseCrud import BaseCrud


class UsersCodeNotify(Document, UserMixin, BaseCrud, Atomic):
    user = ReferenceField('User')
    code = StringField(required=True)
    notify_type = StringField(required=True)
    sent_time = DateTimeField(default=datetime.utcnow)

    meta = {
        "db_alias": "core",
        "collection": "users_code_notify",
        "strict": False,
        "indexes": [
            {
                'fields': ['sent_time'],
                'expireAfterSeconds': 120
            }
        ]
    }

