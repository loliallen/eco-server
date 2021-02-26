from mongoengine import Document, IntField, StringField, ReferenceField, ListField
from exceptions.Product import NotEnoughtCoins
from exceptions.Models import ObjectNotFound

import models.ProductItemTransactionModel as ProductItemTransaction
from .UserModel import User, find_user_by_id
from bson.objectid import ObjectId

class Product(Document):
    ammount = IntField()
    name = StringField()
    items = ListField(ReferenceField('ProductItem'))
    transactions = ListField(ReferenceField('ProductItemTransaction'))
    meta = {
        "db_alias": "core",
        "collection": "products"
    }

def buy(user_id, product_id):
    try:

        user = find_user_by_id(user_id)
        product = find_product_by_id(product_id)

        if product.ammount > user.eco_coins:
            raise NotEnoughtCoins

        # Making status for item
        item = product.items.filter(in_transaction=false).first()
        item.in_transaction = True
        item.save()
        
        # Creating transaction
        transaction = ProductItemTransaction.create(product=product, item=item, user=user)
        product.transactions.append(transaction)
        product.save()

        #
        user.eco_coins -= product.ammount
        user.save() 

        transaction.status = "success"
        transaction.save()

        return transaction

    except NotEnoughtCoins:
        raise NotEnoughtCoins
    finally:
        raise ObjectNotFound(product_id)


def find_product_by_id(product_id:str) -> Product:
    product = Product.objects.get(_id=ObjectId(product_id))
    return product