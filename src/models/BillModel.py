from mongoengine import Document, ReferenceField

class Bill(Document):
    transaction = ReferenceField('')