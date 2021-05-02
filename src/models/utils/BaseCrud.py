from mongoengine import Document
from mongoengine.queryset.queryset import QuerySet


class BaseCrud:

    @classmethod
    def read_(cls) -> QuerySet:
        return cls.objects.all()

    @classmethod
    def create_(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

    @classmethod
    def update_(cls, _id: str, updates: object):
        obj = cls.find_by_id_(_id)
        if not obj:
            return None
        obj.update(**updates)
        obj.save()
        return cls.find_by_id_(obj.id)

    @classmethod
    def delete_(cls, _id: str):
        obj = cls.find_by_id_(_id)
        if not obj:
            return None
        obj.delete()
        return obj

    @classmethod
    def find_by_id_(cls, _id: str):
        return cls.objects(id=_id).first()
