from flask_restful import fields, reqparse
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.product.ProductItemTransactionModel import ProductItemTransaction
from src.utils.roles import jwt_reqired_backoffice


get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')

resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='user.id'),
    'username': fields.String(attribute='user.username'),
    'product_id': fields.String(attribute='product.id'),
    'product_name': fields.String(attribute='product.name'),
    'item_id': fields.String(attribute='item.id'),
    'price': fields.Integer(attribute='amount'),
    'date': fields.DateTime('iso8601')
}


class BuyProductResponseModel(Schema):
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


class BuyProductListController(BaseListController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    @jwt_reqired_backoffice('buy_product', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список всех покупок (Транзакций)', description='-',
                      schema=BuyProductResponseModel)
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(paginate_=True, **args)


class BuyProductController(BaseController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    @jwt_reqired_backoffice('buy_product', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Транзакция', description='-',
                      schema=BuyProductResponseModel)
    def get(self, transaction_id):
        return super().get_(transaction_id)
