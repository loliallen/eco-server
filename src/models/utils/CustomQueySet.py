from bson import json_util
from mongoengine.queryset.queryset import QuerySet

class CustomQuerySet(QuerySet):
        def to_json(self):
            return "[%s]" % (",".join([doc.to_json() for doc in self]))