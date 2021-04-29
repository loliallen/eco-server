from mongoengine import Document, IntField, StringField, ReferenceField, ListField, BooleanField

from bson import ObjectId


class Question(Document):
    value = StringField()
    correct_answer = StringField()

    meta = {
        "db_alias": "core",
        "collection": "question"
    }

def create(data):
    instance = Question(**data)

    instance.save()
    return instance

def read(id=None):
    if id:
        return Question.objects.get(_id=ObjectId(id))

    questions = Question.objects.all()

    return questions
