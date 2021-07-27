from datetime import datetime

from mongoengine import (
    Document, EmbeddedDocument, ReferenceField, FloatField, StringField,
    IntField, DateTimeField, ListField, EmbeddedDocumentField
)

from src.models.transaction.AdmissionTransaction import STATUS_CHOICES, Status
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
    #
    # @classmethod
    # def read_(cls, **kwargs):
    #     status = kwargs.pop('status', None)
    #     if status is None:
    #         return cls.objects.filter(**kwargs).all()
    #     RecPointComment.objects.aggregate([
    #         {''},
    #         {'math'}
    #     ]).filter(**kwargs)
