import datetime

from mongoengine import Document, IntField, StringField, ReferenceField, ListField

from models.product.ProductItemModel import ProductItem
from src.exceptions.Product import NotEnoughtCoins, ProductsIsOver
from src.models.product.ProductItemTransactionModel import ProductItemTransaction
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

    def buy(self, user):
        with user.lock() as user:
            if self.price > user.eco_coins:
                raise NotEnoughtCoins

            item = ProductItem.objects.filter(product=self.id, in_freeze=False, is_active=True, user=None).first()
            if not item:
                raise ProductsIsOver
            with item.lock() as item:
                # Creating transaction
                transaction = ProductItemTransaction.create_(
                    product=self.id,
                    item=item,
                    user=user.id,
                    date=datetime.datetime.utcnow(),
                    amount=self.price
                )
                self.save()
                user.eco_coins -= self.price
                user.save()
                item.update(user=user.id)
                transaction.status = "success"
                transaction.save()
        return transaction
