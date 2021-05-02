from mongoengine import Document, IntField, StringField, ReferenceField, ListField

from exceptions.Models import ObjectNotFound
from src.exceptions.Product import NotEnoughtCoins, ProductsIsOver
from src.models.product.ProductItemTransactionModel import ProductItemTransaction
from src.models.user.UserModel import User
from src.models.utils.BaseCrud import BaseCrud


class Product(Document, BaseCrud):
    price = IntField()
    name = StringField()
    items = ListField(ReferenceField('ProductItem'))
    transactions = ListField(ReferenceField('ProductItemTransaction'))
    meta = {
        "db_alias": "core",
        "collection": "products"
    }

    def buy(self, user_id):
        user = User.find_by_id_(user_id)
        if user is None:
            raise ObjectNotFound('user not found')
        with user.lock() as user:
            if self.price > user.eco_coins:
                raise NotEnoughtCoins

            item = self.items.filter(in_freeze=False, is_active=True, user=None).first()
            if not item:
                raise ProductsIsOver
            with item.lock() as item:
                # Creating transaction
                transaction = ProductItemTransaction.create_(product=self, item=item, user=user)
                self.transactions.append(transaction)
                self.save()
                user.eco_coins -= self.price
                user.save()
                transaction.status = "success"
                transaction.save()
        return transaction
