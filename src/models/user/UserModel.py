from flask_jwt_extended import get_jwt_identity
from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField, ReferenceField
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
    eco_coins = IntField(default=0)  # экокоины, на которые можно покупать товары
    freeze_eco_coins = IntField(default=0)  # замороженные экокоины
    eco_coins_is_avalible = BooleanField(default=False)  # TODO: проверить, используется ли
    code = IntField(default=generate_code)  # код проверки, который отправляется на почту
    qrcode = StringField()  # адрес хранения qrcode изображения
    invite_by_user = ReferenceField('User')
    role = StringField()
    attached_rec_point = ReferenceField('RecPoint')

    token = StringField(default=random_string)  # токен, через который совершаются покупки

    meta = {
        "db_alias": "core",
        "collection": "users"
    }

    def refresh_token(self):
        self.token = random_string()
        self.save()

    @staticmethod
    def get_user_from_request():
        return User.objects.filter(username=get_jwt_identity()).first()
