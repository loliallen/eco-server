from pathlib import Path

from mongoengine import Document, StringField, ListField, ReferenceField

from src.models.utils.BaseCrud import BaseCrud
from src.models.utils.enums import STATUS_CHOICES, Status

REL_PATH = "/statics/recpoints"
files_storage = Path('./src'+REL_PATH)


class Partner(Document, BaseCrud):
    name = StringField(required=True)
    points = ListField(ReferenceField('RecPoint'))
    request_message = StringField()
    status = StringField(choices=STATUS_CHOICES, default=Status.idle.value)
    products = ListField(ReferenceField('Product'))
    user = ReferenceField('User')
    meta = {
        "db_alias": "core",
        "collection": "partners",
        "strict": False
    }

    def __repr__(self):
        return f'<Partner: ({self.id}) {self.name}>'
