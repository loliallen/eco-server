from mongoengine import Document, IntField, StringField, ReferenceField, ListField, BooleanField
from models.ProductModel import find_product_by_id
class ProductItem (Document):
    contents = StringField()
    attached_file = StringField()
    in_transaction = BooleanField(default=false)

    meta = {
        "db_alias": "core",
        "collection": "product_items"
    }

def create(product_id, obj):
    product_item = ProductItem(**obj)
    product_item.save()

    product = find_product_by_id(product_id)

    product.items.append(product_item)

    product.save()
    return product_item
