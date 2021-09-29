import datetime

from mongoengine import Document, StringField, ListField, FloatField, DateTimeField, BooleanField, ReferenceField

from src.models.utils.BaseCrud import BaseCrud


class News(Document, BaseCrud):
    title = StringField()
    text = StringField()
    image = StringField()
    pub_date = DateTimeField(default=datetime.datetime.utcnow)
    is_advice = BooleanField()
    author = ReferenceField('User')
    is_approved = BooleanField()

    meta = {
        "db_alias": "core",
        "collection": "news",
    }

    def __repr__(self):
        return f'<News: ({self.id}) [{self.pub_date}] {self.title}>'
