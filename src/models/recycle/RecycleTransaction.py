from datetime import datetime

from mongoengine import Document, ReferenceField, FloatField, StringField, IntField, DateTimeField

from src.models.transaction.AdmissionTransaction import status_choices
from src.models.utils.BaseCrud import BaseCrud


class RecycleTransaction(Document, BaseCrud):
    """Транзакция сдачи мусора на переработку"""

    from_ = ReferenceField('User')
    to_ = ReferenceField('RecPoint')
    filter_type = ReferenceField('Filter')
    admin_pp = ReferenceField('User')
    image = StringField()
    amount = FloatField(default=0.0)  # Количество сданного материала
    reward = IntField(default=0)  # Количество коинов-вознаграждения
    status = StringField(choices=status_choices, default='i')  # статус подтверждения
    date = DateTimeField(default=datetime.now)

    meta = {
        "db_alias": "core",
        "collection": "recycle_transaction"
    }
