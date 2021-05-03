from flask_restful import reqparse, fields

from controllers.utils.BaseController import BaseListController, BaseController
from models.product.ProductModel import Product

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, location='form')
parser.add_argument('price', type=int, required=True, location='form')

resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'price': fields.Integer,
}


class ProductListController(BaseListController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'
    parser = parser

    def get(self):
        return super().get_()

    def post(self):
        return super().post_()


class ProductController(BaseController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'
    parser = parser

    def get(self, product_id):
        return super().get_(product_id)

    def put(self, product_id):
        return super().put_(product_id)
