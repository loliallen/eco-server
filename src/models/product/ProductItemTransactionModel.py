from mongoengine import Document, ReferenceField, StringField

from models.utils.BaseCrud import BaseCrud


class ProductItemTransaction(Document, BaseCrud):
    product = ReferenceField('Product')
    item = ReferenceField('ProductItem')
    user = ReferenceField('User')

    status = StringField(default="idle")

    meta = {
        "db_alias": "core",
        "collection": "product_item_transactions"
    }
