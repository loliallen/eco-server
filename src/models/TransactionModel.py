from mongoengine import Document, ReferenceField, FloatField, StringField, IntField

from .UserModel import find_user_by_id
from .RecPointModel import find_by_id as find_recpint_by_id
from .FilterModel import find_by_id as find_filter_by_id

from bson.objectid import ObjectId
from src.utils.JsonEncoder import JSONEncoder
import json

status_choices = (
    ('i', 'idle'),
    ('c', 'confimed'),
    ('d', 'dismissed')
)

class Transaction(Document):
    _from = ReferenceField('User')
    _to = ReferenceField('RecPoint')
    filter_type = ReferenceField('Filter')

    image = StringField()
    ammount = FloatField(default=0.0)
    reward = IntField(default=0)
    status = StringField(choices=status_choices, default='i')

    meta = {
        "db_alias": "core",
        "collection": "transactions"
    }
    
    def to_jsony(self):
        self.select_related(max_depth=2)
        data = self.to_mongo()
        if '_from' in data: #reference field
            data['_from'] = self._from.to_mongo() #reference field
        if '_to' in data:
            data['_to'] = self._to.to_mongo()
        if 'filter_type' in data:
            data['filter_type'] = self.filter_type.to_mongo()
        
        return json.loads(json.dumps(data, cls=JSONEncoder))




def read(instance_id = None, instance_type = None):
    if instance_id == None:
        transactions = Transaction.objects.all()
        return transactions
    elif instance_type == 'user':
        transactions = Transaction.objects.filter(_from=ObjectId(instance_id)).all()
        return transactions
    elif instance_type == 'recpoint':   
        transactions = Transaction.objects.filter(_to=ObjectId(instance_id)).all()
        return transactions
    else:
        transactions = Transaction.objects.filter(id=ObjectId(instance_id)).all()
        return transactions
    
def create(user_id, rec_point_id, ammount, filter, image):
    user = find_user_by_id(user_id)
    rec_point = find_recpint_by_id(rec_point_id)
    filter_type = find_filter_by_id(filter)


    transaction = Transaction(_from=user, _to=rec_point, ammount=ammount, image=image, filter_type=filter_type)
    transaction.save()
    confirm(transaction.id, status="c")

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
    return Transaction.objects.get(id=ObjectId(id))