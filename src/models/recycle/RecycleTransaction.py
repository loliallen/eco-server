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
    images = ListField(StringField())
    amount = FloatField(default=0.0)  # Количество сданного материала
    reward = IntField(default=0)  # Количество коинов-вознаграждения
    status = StringField(choices=STATUS_CHOICES, default=Status.idle.value)  # статус подтверждения
    date = DateTimeField(default=datetime.utcnow)

    meta = {
        "db_alias": "core",
        "collection": "recycle_transaction",
        "strict": False
    }

    @staticmethod
    def get_statistic(**kwargs):
        return RecycleTransaction.objects.filter(**kwargs).aggregate([
            # {'$match': {'items': {'$ne': None}}},
            {"$project": {"filter": "$items.filter", "amount": "$items.amount"}},
            {"$unwind": "$filter"},
            {"$unwind": "$amount"},
            {"$group": {"_id": "$filter", "total": {"$sum": "$amount"}}},
            {'$lookup': {'from': 'filters', 'localField': '_id', 'foreignField': '_id', 'as': 'filter_instance'}},
            {"$project": {"_id": 0, "filter": "$_id", 'total': 1, 'name': {'$arrayElemAt': ['$filter_instance.name', 0]}}}
        ])

    @staticmethod
    def get_statistic_by_district(**kwargs):
        return RecycleTransaction.objects.filter(**kwargs).aggregate([
            {'$match': {'items': {'$ne': None}}},
            {'$lookup': {'from': 'rec_points', 'localField': 'to_', 'foreignField': '_id', 'as': 'rec_point'}},
            {"$project": {"district": {'$arrayElemAt': ['$rec_point.district', 0]}, "filter": "$items.filter", "amount": "$items.amount"}},
            {"$unwind": "$filter"},
            {"$unwind": "$amount"},
            {"$group": {"_id": {"filter": "$filter", "district": "$district"}, "total": {"$sum": "$amount"}}},
            {'$lookup': {'from': 'filters', 'localField': '_id.filter', 'foreignField': '_id', 'as': 'filter_instance'}},
            {"$group": {"_id": "$_id.district", "items": {"$push": {"filter": "$_id.filter", "total": "$total", 'name': {'$arrayElemAt': ['$filter_instance.name', 0]}}}}},
            {"$project": {"_id": 0, "district": "$_id", 'items': 1, 'total': { '$sum': '$items.total'}}},
        ])
