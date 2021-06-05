from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController
from src.exceptions.Product import NotEnoughtCoins, ProductsIsOver
from src.models.product.ProductItemTransactionModel import ProductItemTransaction
from src.models.product.ProductModel import Product
from src.models.user.UserModel import User

parser = reqparse.RequestParser()
parser.add_argument('product', type=str, required=True)

resource_fields_ = {
    'id': fields.String,
    'product_id': fields.String(attribute='product.id'),
    'product_name': fields.String(attribute='product.name'),
    'item_id': fields.String(attribute='item.id'),
    'content': fields.String(attribute='item.contents'),
    'amount': fields.Integer,
    #'bill_rest': fields.Integer(attribute='user.eco_coins'),
    'date': fields.DateTime('iso8601')
}


class BuyProductResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id транзакции'},
        'product': {'type': 'string', 'description': 'Id продукта'},
        'item': {'type': 'string', 'description': 'Id  экземпляра купона'},
        'content': {'type': 'string', 'description': 'Содержимое купона'},
        'amount': {'type': 'integer', 'description': 'Стоимость купона'},
        #'bill_rest': {'type': 'integer', 'description': 'Остаток на счету'},
        'date': {'type': 'datetime', 'description': 'Дата транзакции'}
    }


class BuyProductController(BaseListController):
    resource_fields = resource_fields_
    model = ProductItemTransaction
    name = 'ProductItemTransaction'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список всех купонов пользователя', description='-',
                      schema=BuyProductResponseModel)
    def get(self):
        user = User.objects.filter(username=get_jwt_identity()).first()
        return super().get_(user=user.id)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=201, schema=BuyProductResponseModel,
                      summary='Купить продукт (купон)', description='-')
    @swagger.reqparser(name='TransactionCreateModel', parser=parser)
    def post(self):
        args = parser.parse_args()
        product = Product.find_by_id_(args['product'])
        if not product:
            return {'error': 'product not found'}, 404
        user = User.objects.filter(username=get_jwt_identity()).first()
        try:
            trasaction = product.buy(user)
        except NotEnoughtCoins:
            return {'error': 'Not enought coins'}, 400
        except ProductsIsOver:
            return {'error': 'product is over'}, 400
        return marshal(trasaction, resource_fields_)
