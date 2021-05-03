from flask_restful import reqparse, fields, Resource, marshal

from src.exceptions.Product import NotEnoughtCoins, ProductsIsOver
from models.product.ProductModel import Product
from models.user.UserModel import User

parser = reqparse.RequestParser()
parser.add_argument('product', type=str, required=True, location='form')
# TODO: validate user from token
parser.add_argument('user', type=str, required=True, location='form')

resource_fields_ = {
    'product': fields.String,
    'item': fields.String,
    'content': fields.String(attribute=lambda x: x['item'].contents),
    'amount': fields.Integer,
    'bill_rest': fields.Integer(attribute=lambda x: x['user'].eco_coins),
    'date': fields.DateTime
}


class TransactionController(Resource):

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
