from mongoengine import Document, StringField, ListField
from mongoengine.queryset.queryset import QuerySet
from pprint import pprint
from pathlib import Path

import os

REL_PATH = "/static/filters"
files_storage = Path('./src'+REL_PATH)


class Filter(Document):
    """Filter model, using for sort recyclables

    Args:
        Document ([type]): [description]
    """
    name = StringField(required=True)
    var_name = StringField(required=True)
    image = StringField()
    key_words = ListField(StringField())
    bad_words = ListField(StringField())
    meta = {
        "db_alias": "core",
        "collection": "filters"
    }






def read() -> QuerySet:
    """This is functon thats return all filters

    Returns:
        QuerySet: Set of Filter Documents
    """
    filters = Filter.objects.all()
    return filters


def create(name: str, var_name: str, key_words: list, bad_words: list, image: str = "") -> Filter:
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
    fl.key_words = key_words
    fl.bad_words = bad_words
    fl.save()
    print(fl)
    if image != "":
        mime_type = image.split('.')[1]
        filename = str(fl.id) + "." + mime_type 
        img_path = REL_PATH + "/" + filename
        old_path = files_storage / image
        new_path = files_storage / filename
        os.rename(old_path.resolve(), new_path.resolve())
        fl.image = img_path
        print(fl.image)
    # fl.save()
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

def find_filter_by_key_words(key_words: []):
    if not key_words:
        return None

    filters = Filter.objects.all()
    filters_list = []

    for filter in filters:
        for word in filter.key_words:
            flag = False
            words = word.split(" ")
            for key_word in key_words:
                flag = False
                for word1 in words:
                    if word1.find(key_word) != -1:
                        filters_list.append(filter.id)
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break

    return filters_list