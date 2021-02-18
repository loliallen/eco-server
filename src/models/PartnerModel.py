from mongoengine import Document, StringField, ListField

from mongoengine.fields import ReferenceField
from mongoengine.queryset.queryset import QuerySet
from pprint import pprint

from src.models.RecPointModel import Partner



def read() -> QuerySet:
    """This is functon thats return all partners
    Returns:
        QuerySet: Set of Partner Documents
    """
    partners = Partner.objects.all()
    return partners


def create(name: str) -> Partner:
    """This is functon thats creates partner

    Returns:
        Filter: Created partner
    """
    pn = Partner()
    pn.name = name
    pn.save()
    return pn


def update(_id: str, updates: object) -> Partner:
    """This is functon thats updates partner
    Args:
        _id (str): - partner id
        updates (object) - Updates
        updates.name (str): partner new name
        updates.points [ObjectId]: RecPoints id
    Returns:
        RecPoint: Updated RecPoint
    """
    pn = Partner.objects(id=_id).first()
    if not pn:
        return None
    pn.update(**updates)
    return pn


def delete(_id: str) -> Partner:
    """This is functon thats deletes partner

    Returns:
        RecPoint: Deleted partner
    """
    pn = Partner.objects(id=_id).first()
    if not pn:
        return None
    pn.delete()
    return pn

def find_by_id(_id: str) -> Partner:
    partner = Partner.objects(id=_id).first()
    if not partner:
        return None
    return partner