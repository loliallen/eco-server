from flask_restful import inputs
from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.models.user.UserModel import User
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.product.ProductModel import Product
from src.utils.roles import jwt_reqired_backoffice, Roles

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


Date = inputs.date
Date.swagger_type = 'date'


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Название продукта')
parser.add_argument('price', type=int, required=True, help='Стоимость продукта')
parser.add_argument('date_from', type=Date, required=True, help='Срок действия с')
parser.add_argument('date_to', type=Date, required=True, help='Срок действия по')
parser.add_argument('is_active', type=bool, required=False, help='Активность продукта (можно ли его купить)')


class ProductResponseModelAdmin(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id продукта'},
        'name': {'type': 'string', 'description': 'Название продукта'},
        'price': {'type': 'integer', 'description': 'Стоимость продукта'},
        'date_from': {'type': 'string', 'format': 'date', 'description': 'Срок действия с'},
        'date_to': {'type': 'string', 'format': 'date',  'description': 'Срок действия по'},
        'is_active': {'type': 'boolean', 'description': 'Активность продукта (можно ли его купить)'},
        'image': {'type': 'string', 'description': 'Иконка'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'price': fields.Integer,
    'date_from': fields.DateTime('iso8601'),
    'date_to': fields.DateTime('iso8601'),
    'is_active': fields.Boolean,
    'image': custom_fields.ImageLink,
}


class ProductListController(BaseListController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'
    parser = parser

    @jwt_reqired_backoffice('product', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список продуктов (купонов)', description='-', schema=ProductResponseModelAdmin)
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        admin = User.get_user_from_request()
        if Roles(admin.role) == Roles.partner:
            args['partner'] = admin
        return super().get_(paginate_=True, **args)

    @jwt_reqired_backoffice('product', 'create')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=201, schema=ProductResponseModelAdmin, summary='Создать новый продукт (купон)', description='-')
    @swagger.reqparser(name='ProductCreateModel', parser=parser)
    def post(self):
        args = {}
        admin = User.get_user_from_request()
        if Roles(admin.role) == Roles.partner:
            args['partner'] = admin
        return super().post_(**args)


class ProductController(BaseController):
    resource_fields = resource_fields_
    model = Product
    name = 'Product'
    parser = parser

    @jwt_reqired_backoffice('product', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Продукт (купон)', description='-', schema=ProductResponseModelAdmin)
    def get(self, product_id):
        args = {}
        admin = User.get_user_from_request()
        if Roles(admin.role) == Roles.partner:
            args['partner'] = admin
        return super().get_(product_id, **args)

    @jwt_reqired_backoffice('product', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Обновить продукт (купон)', description='-', schema=ProductResponseModelAdmin)
    @swagger.reqparser(name='ProductPutModel', parser=parser)
    def put(self, product_id):
        args = {}
        admin = User.get_user_from_request()
        if Roles(admin.role) == Roles.partner:
            args['partner'] = admin
        return super().put_(product_id, **args)
