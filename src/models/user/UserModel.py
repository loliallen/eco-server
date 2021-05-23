from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField
from pathlib import Path
from flask_login import UserMixin

from src.models.utils.Atomic import Atomic
from src.models.utils.BaseCrud import BaseCrud
from src.utils.generator import random_string, generate_code

REL_PATH = "/statics/users"
files_storage = Path('./src'+REL_PATH)


class User(Document, UserMixin, BaseCrud, Atomic):
    username = StringField(required=True, unique=True)
    name = StringField(required=True)
    surname = StringField()
    password = StringField(required=True)
    image = StringField()
    confirmed = BooleanField(default=False)
    confirmed_on = DateTimeField()
    eco_coins = IntField(default=0)
    eco_coins_is_avalible = BooleanField(default=False)
    code = IntField(default=generate_code)
    qrcode = StringField()

    token = StringField(default=random_string)

    meta = {
        "db_alias": "core",
        "collection": "users"
    }

    def refresh_token(self):
        self.token = random_string()
        self.save()
