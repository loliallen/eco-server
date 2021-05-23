from flask_restful import fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.product.ProductItemTransactionModel import ProductItemTransaction

resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='user.id'),
    'username': fields.String(attribute='user.username'),
    'product_id': fields.String(attribute='product.id'),
    'product_name': fields.String(attribute='product.name'),
    'item_id': fields.String(attribute='item.id'),
    'price': fields.Integer(attribute='amount'),
    'date': fields.DateTime
}


class TransactionItemResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id транзакции'},
        'user_id': {'type': 'string', 'description': 'Id пользователя'},
        'username': {'type': 'string', 'description': 'Имя пользователя'},
        'product_id': {'type': 'string', 'description': 'Id продукта'},
        'product_name': {'type': 'string', 'description': 'Имя продукта'},
        'item_id': {'type': 'string', 'description': 'Id экземпляра продукта'},
        'price': {'type': 'string', 'description': 'Цена продукта'},
        'date': {'type': 'datetime', 'description': 'Дата транзакции'}
    }


class TransactionListController(BaseListController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список всех транзакций', description='-',
                      schema=TransactionItemResponseModel)
    def get(self):
        return super().get_()


class TransactionController(BaseController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Транзакция', description='-',
                      schema=TransactionItemResponseModel)
    def get(self, transaction_id):
        return super().get_(transaction_id)
