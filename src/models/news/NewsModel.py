import datetime

from mongoengine import Document, StringField, ListField, FloatField, DateTimeField, BooleanField

from src.models.utils.BaseCrud import BaseCrud


class News(Document, BaseCrud):
    title = StringField()
    text = StringField()
    # image = StringField()
    pub_date = DateTimeField(default=datetime.datetime.utcnow)
    is_advice = BooleanField()

    meta = {
        "db_alias": "core",
        "collection": "news",
    }
