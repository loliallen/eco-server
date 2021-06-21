from enum import Enum
from datetime import datetime

from mongoengine import Document, ReferenceField, FloatField, StringField, IntField, GenericReferenceField, \
    DateTimeField

from src.models.user.UserModel import User
from src.models.utils.BaseCrud import BaseCrud


class ActionType(Enum):
    recycle = 'recycle'
    invite = 'invite'
    feedback = 'feedback'


class Status(Enum):
    idle = 'idle'
    confirmed = 'confimed'
    dismissed = 'dismissed'


ACTION_TYPE_CHOICES = ('recycle', 'invite', 'feedback')
STATUS_CHOICES = ('idle', 'confimed', 'dismissed')


class AdmissionTransaction(Document, BaseCrud):
    """Транзакция зачисления экокоинов"""

    action_type = StringField(choices=ACTION_TYPE_CHOICES)
    action = GenericReferenceField()
    user = ReferenceField('User')
    eco_coins = IntField()
    status = StringField(choices=STATUS_CHOICES, default=Status.idle.value)  # статус подтверждения
    date = DateTimeField(default=datetime.now)

    meta = {
        "db_alias": "core",
        "collection": "admission_transacrion",
        "strict": False
    }

    @classmethod
    def create_and_pay_for_user(cls, **kwargs):
        super().create_(**kwargs)
        User.find_by_id_(_id=kwargs['user']).add_freeze_coins(kwargs['eco_coins'])

    def unlock(self):
        with self.user.lock() as user:
            if user.freeze_eco_coins < self.eco_coins:
                raise Exception('замороженных эко коинов на счету меньше, чем сумма транзакции')
            user.freeze_eco_coins -= self.eco_coins
            user.eco_coins += self.eco_coins
            user.save()
            self.status = Status.confirmed.value
            self.save()
