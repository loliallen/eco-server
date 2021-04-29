from mongoengine import Document, ReferenceField, StringField

class ProductItemTransaction(Document):
    product = ReferenceField('Product')
    item = ReferenceField('ProductItem')
    user = ReferenceField('User')

    status = StringField(default="idle")

    meta = {
        "db_alias": "core",
        "collection": "product_item_transactions"
    }


def create(product, item, user):
    transaction = ProductItemTransaction(
        product=product,
        item=item,
        user=user,
    )
    transaction.save()
    return transaction