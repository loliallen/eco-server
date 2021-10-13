import datetime

from flask import current_app as app
from mongoengine import Document, IntField, StringField, ReferenceField, ListField, BooleanField, DateField

from src.exceptions.Product import NotEnoughtCoins, ProductsIsOver
from src.models.product.ProductItemModel import ProductItem
from src.models.product.ProductItemTransactionModel import ProductItemTransaction
from src.models.utils.BaseCrud import BaseCrud


class Product(Document, BaseCrud):
    price = IntField()
    name = StringField()
    date_from = DateField()
    date_to = DateField()
    is_active = BooleanField(default=False)
    partner = ReferenceField('User')
    items = ListField(ReferenceField('ProductItem'))
    transactions = ListField(ReferenceField('ProductItemTransaction'))
    image = StringField()

    meta = {
        "db_alias": "core",
        "collection": "products",
        "strict": False,
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
        app.logger.info(f'{item} was buy by {user} ({transaction})')
        return transaction

    @staticmethod
    def get_product_with_count(**kwargs):
        """Запрос на продукты с полем количество продукта данного типа"""
        return Product.objects.filter(**kwargs).aggregate({
            "$lookup": {
                "from": "product_items",
                "foreignField": "product",
                "localField": "_id",
                "as": "product_items",
                # 'pipeline': {
                #     '$filter': {
                #         'user': {'$exists': False}
                #     }
                # }
            }},
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'price': 1,
                    'date_from': 1,
                    'date_to': 1,
                    'count': {'$size': "$product_items"},
                }
            }
        )

    def __repr__(self):
        return f'<Product: ({self.id}) {self.name}>'
