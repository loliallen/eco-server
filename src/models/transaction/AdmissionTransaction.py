from enum import Enum
from datetime import datetime

from mongoengine import Document, ReferenceField, FloatField, StringField, IntField, GenericReferenceField, \
    DateTimeField

from src.models.user.UserModel import User
from src.models.utils.BaseCrud import BaseCrud


class ActionType(Enum):
    recycle = 'r'
    invite = 'i'
    feedback = 'f'


action_type_choices = (
    ('r', 'recycle'),
    ('i', 'invite'),
    ('f', 'feedback')
)


class Status(Enum):
    idle = 'i'
    confirmed = 'c'
    dismissed = 'd'


status_choices = (
    ('i', 'idle'),
    ('c', 'confimed'),
    ('d', 'dismissed')
)


class AdmissionTransaction(Document, BaseCrud):
    """Транзакция зачисления эко коинов"""

    action_type = StringField(choices=action_type_choices)
    action = GenericReferenceField()
    user = ReferenceField('User')
    eco_coins = IntField()
    status = StringField(choices=status_choices, default='i')  # статус подтверждения
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
            self.status = 'c'
            self.save()
