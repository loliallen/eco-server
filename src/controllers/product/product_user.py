import datetime

from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController, not_found
from src.models.product.ProductModel import Product, ProductItem


class ProductResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id продукта'},
        'name': {'type': 'string', 'description': 'Название продукта'},
        'price': {'type': 'integer', 'description': 'Стоимость продукта'},
        'date_from': {'type': 'string', 'format': 'date', 'description': 'Срок действия с'},
        'date_to': {'type': 'string', 'format': 'date', 'description': 'Срок действия по'},
        'days_rest': {'type': 'integer', 'description': 'Количество оставшихся дней действия продукта'},
        'count': {'type': 'integer', 'description': 'Количество оставшегося продукта'},
        # TODO добавить количество оставшихся купонов
    }


resource_fields_ = {
    'id': fields.String(attribute='_id'),
    'name': fields.String,
    'price': fields.Integer,
    'count': fields.Integer,
    'date_from': fields.DateTime('iso8601'),
    'date_to': fields.DateTime('iso8601'),
    'days_rest': fields.Integer(attribute=lambda x: (x['date_to'].date() - datetime.datetime.now().date()).days),
}


class ProductListController(BaseListController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список продуктов (купонов)', description='-',
                      schema=ProductResponseModel)
    def get(self):
        return marshal(list(Product.get_product_with_count(is_active=True)), self.resource_fields)


class ProductController(BaseController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Продукт (купон)', description='-', schema=ProductResponseModel)
    def get(self, product_id):
        obj = Product.get_product_with_count(id=product_id, is_active=True).first()
        if not obj:
            return not_found(self.name, id)
        return marshal(obj, self.resource_fields)
