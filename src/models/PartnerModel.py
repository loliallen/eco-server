from mongoengine import Document, StringField, ListField
from mongoengine.queryset.queryset import QuerySet
from pprint import pprint


class Partner(Document):
    name = StringField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "partners"
    }


def read() -> Partner:
    """This is functon thats return all filters

    Returns:
        QuerySet: Set of Filter Documents
    """
    partners = Partner.objects.all()
    return partners


def create(name: str) -> Partner:
    """This is functon thats creates filter

    Args:
        name (str): Filter name
        var_name (str): Filter varible name
        image (str, optional): Filter icon. Defaults to "".

    Returns:
        Filter: Created filter
    """
    pn = Partner()
    pn.name = name
    pn.save()
    return pn


def update(_id: str, updates: object) -> Partner:
    """This is functon thats updates filter

    Args:
        _id (str): - Filter id
        updates (object) - Updates
        updates.name (str): Filter new name
        updates.var_name (str): Filter varible name
        updates.image (str): Filter icon
        updates.key_words (str[]): Filter key_words

    Returns:
        Filter: Updated filter
    """
    pn = Partner.objects(id=_id).first()
    if not pn:
        return None
    pn.update(**updates)
    return pn


def delete(_id: str) -> Partner:
    """This is functon thats deletes filter

    Args:
        _id (str): Filter id

    Returns:
        Filter: Deleted filter
    """
    pn = Partner.objects(id=_id).first()
    if not pn:
        return None
    pn.delete()
    return pn