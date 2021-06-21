from mongoengine import Document, StringField, IntField, ListField, ReferenceField

from src.models.test.Test import Test
from src.models.utils.BaseCrud import BaseCrud


QUESTION_TYPE_CHOICES = ('open', 'choices')


class Question(Document, BaseCrud):
    question = StringField()
    image = StringField()
    test = ReferenceField(Test, required=True)
    question_type = StringField(choices=QUESTION_TYPE_CHOICES)
    answers_variants = ListField(StringField())
    correct_answer = StringField()
    description = StringField()
    point_for_answer = IntField()

    meta = {
        "db_alias": "core",
        "collection": "question",
        "strict": False,
    }
