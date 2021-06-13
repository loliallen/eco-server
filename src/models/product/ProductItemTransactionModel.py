from mongoengine import Document, ReferenceField, StringField, DateTimeField, IntField

from src.models.utils.BaseCrud import BaseCrud


class ProductItemTransaction(Document, BaseCrud):
    product = ReferenceField('Product', required=True)
    item = ReferenceField('ProductItem', required=True)
    user = ReferenceField('User', required=True)
    date = DateTimeField(required=True)
    amount = IntField(required=True)

    status = StringField(default="idle")

    meta = {
        "db_alias": "core",
        "collection": "product_item_transactions",
        "strict": False,
    }
