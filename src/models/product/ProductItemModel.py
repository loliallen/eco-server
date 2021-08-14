from mongoengine import Document, StringField, ReferenceField, BooleanField

from src.models.user.UserModel import User
from src.models.utils.Atomic import Atomic
from src.models.utils.BaseCrud import BaseCrud


class ProductItem(Document, BaseCrud, Atomic):
    product = ReferenceField('Product')
    partner = ReferenceField('User')
    contents = StringField()
    attached_file = StringField()  # TODO: проверить нужно ли это поле
    is_active = BooleanField(default=False)
    user = ReferenceField(User)

    meta = {
        "db_alias": "core",
        "collection": "product_items",
        "strict": False,
    }
