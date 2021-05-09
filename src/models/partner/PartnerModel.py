from pathlib import Path

from mongoengine import Document, StringField, ListField, ReferenceField

from src.models.utils.BaseCrud import BaseCrud

REL_PATH = "/statics/recpoints"
files_storage = Path('./src'+REL_PATH)


class Partner(Document, BaseCrud):
    name = StringField(required=True)
    points = ListField(ReferenceField('RecPoint'))
    products = ListField(ReferenceField('Product'))
    meta = {
        "db_alias": "core",
        "collection": "partners"
    }
