from flask_restful import marshal
from mongoengine.queryset.base import BaseQuerySet


def paginate(query: BaseQuerySet, page, size, resource_fields, select_related_depth=0):
    count = query.count()
    data = query.skip((page-1) * size).limit(size)
    if select_related_depth > 0:
        data = data.select_related(max_depth=select_related_depth)
    return {
        "data": marshal(list(data), resource_fields),
        "count": count,
        "page": page,
        "size": size,
    }

