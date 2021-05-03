from mongoengine import Document, StringField, ReferenceField, BooleanField

from models.user.UserModel import User
from controllers.utils.Atomic import Atomic
from models.utils.BaseCrud import BaseCrud


class ProductItem(Document, BaseCrud, Atomic):
    product = ReferenceField('Product')
    contents = StringField()
    attached_file = StringField()
    is_active = BooleanField(default=True)
    user = ReferenceField(User)

    meta = {
        "db_alias": "core",
        "collection": "product_items"
    }
