from datetime import datetime

from mongoengine import (
    Document, ReferenceField, StringField,
    DateTimeField, ListField
)

from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.utils.BaseCrud import BaseCrud


class RecPointComment(Document, BaseCrud):
    """Комментарий к пункту приема"""

    user = ReferenceField('User')
    rec_point = ReferenceField('RecPoint')
    type = ListField(StringField())
    text = StringField()
    transaction = ReferenceField('AdmissionTransaction')
    date = DateTimeField(default=datetime.utcnow)
    images = ListField(StringField())

    meta = {
        "db_alias": "core",
        "collection": "rec_point_comments",
        "strict": False
    }

    @classmethod
    def read_(cls, **kwargs):
        status = kwargs.pop('status', None)
        q = RecPointComment.objects
        if status is not None:
            q = q.filter(transaction__in=AdmissionTransaction.objects(status='idle'))
        q = q.filter(**kwargs)
        return q
