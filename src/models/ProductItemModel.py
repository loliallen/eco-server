from mongoengine import Document, IntField, StringField, ReferenceField, ListField, BooleanField



class ProductItem (Document):
    contents = StringField()
    attached_file = StringField()
    in_transaction = BooleanField(default=False)

    meta = {
        "db_alias": "core",
        "collection": "product_items"
    }

def create(product, obj):
    product_item = ProductItem(**obj)
    product_item.save()


    product.items.append(product_item)

    product.save()
    return product_item
