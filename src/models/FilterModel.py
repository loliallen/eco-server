from flask import jsonify
from mongoengine import Document, StringField, ListField
from mongoengine.queryset.queryset import QuerySet
from pprint import pprint

from utils.mongo import dict_to_update

class Filter(Document):
    """Filter model, using for sort recyclables

    Args:
        Document ([type]): [description]
    """
    name = StringField(required=True)
    var_name = StringField(required=True)
    image = StringField()
    key_words = ListField(StringField(max_length=30))
    meta = {
        "db_alias": "core",
        "collection": "filters"
    }


def read() -> QuerySet:
    """This is functon thats return all filters

    Returns:
        QuerySet: Set of Filter Documents
    """
    filters = Filter.objects.exclude("key_words")
    return filters


def create(name: str, var_name: str, image: str = "") -> Filter:
    """This is functon thats creates filter

    Args:
        name (str): Filter name
        var_name (str): Filter varible name 
        image (str, optional): Filter icon. Defaults to "".

    Returns:
        Filter: Created filter
    """
    fl = Filter()
    fl.name = name
    fl.var_name = var_name
    if image != "":
        fl.image = image
    fl.save()
    return fl


def update(_id: str, updates: object) -> Filter:
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
    fl = find_by_id(_id)
    if not fl:
        return None
    fl.update(**updates)
    return fl

def delete(_id: str) -> Filter:
    """This is functon thats deletes filter

    Args:
        _id (str): Filter id

    Returns:
        Filter: Deleted filter
    """
    fl = find_by_id(_id)
    if not fl:
        return None
    fl.delete()
    return fl

def find_by_id(_id: str) -> Filter:
    print(_id)
    fl = Filter.objects(id=_id).first()
    if not fl:
        return None
    pprint(fl.to_json())
    return fl

def append_key_word_by_id(_id: str, new_key_word: str) -> Filter:
    fl = find_by_id(_id)
    if not fl:
        return None
    fl.update(add_to_set__key_word=new_key_word)
    return fl