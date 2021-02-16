from src.models.FilterModel import Filter
from mongoengine import Document
from mongoengine.fields import ReferenceField, StringField
from mongoengine.queryset.queryset import QuerySet
from pathlib import Path
import os


REL_PATH = "/static/markers"
files_storage = Path('./src'+REL_PATH)

class Marker(Document):
    filter_vname = StringField() 
    image = StringField()
    description = StringField()
    meta = {
        "db_alias": "core",
        "collection": "markers"
    }

def read() -> QuerySet:
    markers = Marker.objects.all()

    return markers

def create(data, image=None):
    marker = Marker(**data)
    marker.save()

    if image != None:
        mime_type = image.split('.').pop()
        filename = str(marker.id) + "." + mime_type 
        img_path = REL_PATH + "/" + filename
        old_path = files_storage / image
        new_path = files_storage / filename
        os.rename(old_path.resolve(), new_path.resolve())
        marker.image = img_path
        marker.save()

    return marker


def update(_id: str, updates: object) -> Marker:

    fl = find_by_id(_id)
    if not fl:
        return None
    fl.update(**updates)
    return fl

def delete(_id: str) -> Marker:

    fl = find_by_id(_id)
    if not fl:
        return None
    fl.delete()
    return fl


def find_by_id(_id: str) -> Marker:
    
    fl = Marker.objects(id=_id).first()
    if not fl:
        return None
    return fl
