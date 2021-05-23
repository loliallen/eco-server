from mongoengine import Document, StringField, IntField, ListField, ReferenceField

from src.models.test.Test import Test
from src.models.utils.BaseCrud import BaseCrud


class Question(Document, BaseCrud):
    question = StringField()
    image = StringField()
    test = ReferenceField(Test, required=True)
    question_type = StringField()
    answers_variants = ListField(StringField())
    correct_answer = StringField()
    point_for_answer = IntField()

    meta = {
        "db_alias": "core",
        "collection": "question"
    }
