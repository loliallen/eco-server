from flask_restful import fields

from controllers.utils.BaseController import BaseListController, BaseController
from models.product.ProductItemTransactionModel import ProductItemTransaction

resource_fields_ = {
    'user_id': fields.String('user.id'),
    'username': fields.String(attribute='user.username'),
    'product_id': fields.String(attribute='product.id'),
    'product_name': fields.String(attribute='product.name'),
    'item_id': fields.String(attribute='item.id'),
    'price': fields.Integer(attribute='amount'),
    'date': fields.DateTime
}


class TransactionListController(BaseListController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    def get(self):
        return super().get_()


class TransactionController(BaseController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    def get(self, product_id):
        return super().get_(product_id)
