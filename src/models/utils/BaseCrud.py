import bson
from bson import ObjectId
from mongoengine import ReferenceField, ListField
from mongoengine.queryset.queryset import QuerySet

from src.exceptions.common import FieldError


class BaseCrud:
    @classmethod
    def read_(cls, **kwargs) -> QuerySet:
        q = cls.objects
        if 'search' in kwargs:
            value = kwargs.pop('search')
            q = q.filter(cls.search_q(value))
        return q.filter(**kwargs).all()

    @classmethod
    def create_(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

    @classmethod
    def update_(cls, _id: str, updates: dict, **kwargs):
        obj = cls.find_by_id_(_id, **kwargs)
        if not obj:
            return None
        ref_fields = [k for k, v in cls._fields.items() if isinstance(v, ReferenceField)]
        def process_value(value):
            if isinstance(value, dict):
                value = value['$oid']
            return ObjectId(value)

        for field_name in ref_fields:
            value = updates.get(field_name)
            if value:
                try:
                    updates[field_name] = process_value(value)
                except bson.errors.InvalidId:
                    raise FieldError(field_name, 'bad format')
        ref_list_fields = [k for k, v in cls._fields.items() if isinstance(v, ListField) and isinstance(v.field, ReferenceField)]
        for field_name in ref_list_fields:
            values = updates.get(field_name)
            if values:
                try:
                    updates[field_name] = [process_value(value) for value in values]
                except bson.errors.InvalidId:
                    raise FieldError(field_name, 'bad format')
        obj.update(**updates)
        obj.save()
        return cls.find_by_id_(obj.id)

    @classmethod
    def delete_(cls, _id: str, **kwargs):
        obj = cls.find_by_id_(_id, **kwargs)
        if not obj:
            return None
        obj.delete()
        return obj

    @classmethod
    def find_by_id_(cls, _id: str, **kwargs):
        return cls.objects(id=_id, **kwargs).first()

    @classmethod
    def search_q(cls, value) -> object:
        raise NotImplementedError
