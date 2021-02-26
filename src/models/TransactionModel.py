from mongoengine import Document, ReferenceField, FloatField, StringField, IntField

from .UserModel import find_user_by_id
from .RecPointModel import find_by_id as find_recpint_by_id

from bson.objectid import ObjectId

status_choices = (
    ('i', 'idle'),
    ('c', 'confimed'),
    ('d', 'dismissed')
)

class Transaction(Document):
    _from = ReferenceField('User')
    _to = ReferenceField('RecPoint')

    image = StringField()
    ammount = FloatField(default=0.0)
    reward = IntField(default=0)
    status = StringField(choices=status_choices)

    meta = {
        "db_alias": "core",
        "collection": "transactions"
    }




def read():
    transactions = Transaction.objects.all()

    return transactions


def create(user_id, rec_point_id, ammount):
    user = find_user_by_id(user_id)
    rec_point = find_recpint_by_id(rec_point_id)


    transaction = Transaction(_from=user, _to=rec_point, ammount=ammount)
    transaction.save()

    return transaction

def confirm(transaction_id, status):
    transaction = find_transaction_by_id(transaction_id)
    transaction.status = status
    if status == 'c':
        user = transaction._from
        user.eco_coins += transaction.ammount
        user.save()

    transaction.save()
    return transaction


def find_transaction_by_id(id) -> Transaction:
    return Transaction.objects.get(_id=ObjectId(id))