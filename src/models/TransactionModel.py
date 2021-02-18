from mongoengine import Document, ReferenceField, FloatField, StringField, IntField

# from .UserModel import 

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



def read():
    transactions = Transaction.objects.all()

    return transactions


def create(_from, _to, ammount):
    transaction = Transaction(_from=_from, _to=_to, ammount=ammount)
    transaction.save()