from flask_restful import reqparse, fields, Resource, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.exceptions.Product import NotEnoughtCoins, ProductsIsOver
from src.models.product.ProductModel import Product
from src.models.user.UserModel import User

parser = reqparse.RequestParser()
parser.add_argument('product', type=str, required=True)
# TODO: validate user from token
parser.add_argument('user', type=str, required=True)

resource_fields_ = {
    'id': fields.String,
    'product': fields.String,
    'item': fields.String,
    'content': fields.String(attribute='item.contents'),
    'amount': fields.Integer,
    'bill_rest': fields.Integer(attribute='user.eco_coins'),
    'date': fields.DateTime
}


class TransactionItemResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'product': {'type': 'string'},
        'item': {'type': 'string'},
        'content': {'type': 'string'},
        'amount': {'type': 'integer'},
        'bill_rest': {'type': 'integer'},
        'date': {'type': 'datetime'}
    }


class TransactionController(Resource):

    @swagger.tags('Transactions')
    @swagger.response(response_code=201, schema=TransactionItemResponseModel,
                      summary='Создать новый экземпляр продукта (купон)', description='-')
    @swagger.reqparser(name='TransactionCreateModel', parser=parser)
    def post(self):
        args = parser.parse_args()
        product = Product.find_by_id_(args['product'])
        if not product:
            return {'error': 'product not found'}, 404
        user = User.find_by_id_(args['user'])
        if user is None:
            return {'error': 'user not found'}, 404
        try:
            trasaction = product.buy(user)
        except NotEnoughtCoins:
            return {'error': 'Not enought coins'}, 400
        except ProductsIsOver:
            return {'error': 'product is over'}, 400
        return marshal(trasaction, resource_fields_)
