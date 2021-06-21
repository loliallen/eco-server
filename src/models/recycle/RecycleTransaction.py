from datetime import datetime

from mongoengine import (
    Document, EmbeddedDocument, ReferenceField, FloatField, StringField,
    IntField, DateTimeField, ListField, EmbeddedDocumentField
)

from src.models.transaction.AdmissionTransaction import STATUS_CHOICES, Status
from src.models.utils.BaseCrud import BaseCrud


class RecycleTransactionItem(EmbeddedDocument):
    filter = ReferenceField('Filter')
    amount = FloatField(default=0.0)


class RecycleTransaction(Document, BaseCrud):
    """Транзакция сдачи мусора на переработку"""

    from_ = ReferenceField('User')
    to_ = ReferenceField('RecPoint')
    items = ListField(EmbeddedDocumentField(RecycleTransactionItem))
    filter_type = ReferenceField('Filter')
    admin_pp = ReferenceField('User')
    image = StringField()
    amount = FloatField(default=0.0)  # Количество сданного материала
    reward = IntField(default=0)  # Количество коинов-вознаграждения
    status = StringField(choices=STATUS_CHOICES, default=Status.idle.value)  # статус подтверждения
    date = DateTimeField(default=datetime.now)

    meta = {
        "db_alias": "core",
        "collection": "recycle_transaction",
        "strict": False
    }
