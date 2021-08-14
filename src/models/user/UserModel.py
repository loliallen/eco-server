import datetime

from flask_jwt_extended import get_jwt_identity
from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField, ReferenceField
from flask_login import UserMixin

from src.models.utils.Atomic import Atomic
from src.models.utils.BaseCrud import BaseCrud
from src.utils.generator import random_string, generate_code
from src.utils.roles import get_role_schema, Roles


class User(Document, UserMixin, BaseCrud, Atomic):
    username = StringField(required=True, unique=True)
    name = StringField(required=True)
    surname = StringField()
    password = StringField(required=True)
    image = StringField()
    confirmed = BooleanField(default=False)
    register_on = DateTimeField(default=datetime.datetime.utcnow)
    confirmed_on = DateTimeField()
    last_login = DateTimeField()
    eco_coins = IntField(default=0)  # экокоины, на которые можно покупать товары
    freeze_eco_coins = IntField(default=0)  # замороженные экокоины
    code = IntField(default=generate_code)  # код проверки, который отправляется на почту
    qrcode = StringField()  # адрес хранения qrcode изображения
    invite_by_user = ReferenceField('User')
    role = StringField(default="user")  # TODO: сделать энамом
    attached_rec_point = ReferenceField('RecPoint')

    token = StringField(default=random_string)  # токен, через который совершаются покупки

    meta = {
        "db_alias": "core",
        "collection": "users",
        "strict": False
    }

    def refresh_token(self):
        self.token = random_string()
        self.save()

    @staticmethod
    def get_user_from_request():
        return User.objects.filter(username=get_jwt_identity()).first()

    def add_freeze_coins(self, coins):
        with self.lock() as user:
            user.update(inc__freeze_eco_coins=coins)

    @staticmethod
    def get_statistic(**kwargs):
        period = kwargs.pop('period', None)
        group_by = {'year': {'$year': '$confirmed_on'}}
        if period in ['month', 'week', 'day']:
            group_by['month'] = {'$month': '$confirmed_on'}
        if period == 'week':
            group_by["weekOfMonth"] = {'$floor': {'$divide': [{'$dayOfMonth': "$confirmed_on"}, 7]}}
        if period == 'day':
            group_by['day'] = {'$dayOfMonth': '$confirmed_on'}
        return User.objects.filter(**kwargs).aggregate([
            # {'$match': {'confirmed_on': {'$ne': None}}},
            {'$group': {
                '_id': group_by,
                'cnt': {'$sum': 1}}},
            {'$sort': {'_id': 1}}
        ])

    @property
    def access_schema(self):
        return get_role_schema(Roles(self.role))
