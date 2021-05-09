from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.product.ProductModel import Product

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('price', type=int, required=True)
parser.add_argument('is_active', type=bool, required=True)


class ProductResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'price': {'type': 'integer'},
        'is_active': {'type': 'boolean'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'price': fields.Integer,
    'is_active': fields.Boolean
}


class ProductListController(BaseListController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'
    parser = parser

    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список продуктов (купонов)', description='-', schema=ProductResponseModel)
    def get(self):
        return super().get_()

    @swagger.tags('Products')
    @swagger.response(response_code=201, schema=ProductResponseModel, summary='Создать новый продукт (купон)', description='-')
    @swagger.reqparser(name='ProductCreateModel', parser=parser)
    def post(self):
        return super().post_()


class ProductController(BaseController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'
    parser = parser

    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Продукт (купон)', description='-', schema=ProductResponseModel)
    def get(self, product_id):
        return super().get_(product_id)

    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Обновить продукт (купон)', description='-', schema=ProductResponseModel)
    @swagger.reqparser(name='ProductPutModel', parser=parser)
    def put(self, product_id):
        return super().put_(product_id)
