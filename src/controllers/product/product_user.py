from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.product.ProductModel import Product


class ProductResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id продукта'},
        'name': {'type': 'string', 'description': 'Название продукта'},
        'price': {'type': 'integer', 'description': 'Стоимость продукта'}
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

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список продуктов (купонов)', description='-', schema=ProductResponseModel)
    def get(self):
        return super().get_(is_active=True)


class ProductController(BaseController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Продукт (купон)', description='-', schema=ProductResponseModel)
    def get(self, product_id):
        return super().get_(product_id, is_active=True)
