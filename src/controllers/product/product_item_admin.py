from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController, not_found
from src.models.product.ProductItemModel import ProductItem
from src.utils.roles import jwt_reqired_backoffice


get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


parser = reqparse.RequestParser()
parser.add_argument('product', type=str, required=True, help='id продукта')
parser.add_argument('contents', type=str, required=True, help='Содержимое купона (ключ)')
parser.add_argument('is_active', type=bool, help='Активность, отвечает за показ пользователям')

resource_fields_ = {
    'id': fields.String,
    'product_id': fields.String(attribute='product.id'),
    'product_name': fields.String(attribute='product.name'),
    'contents': fields.String,
    'is_active': fields.Boolean,
    'is_bought': fields.Boolean(attribute=lambda x: bool(x.user))
}


class ProductItemResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'product_id': {'type': 'string'},
        'product_name': {'type': 'string'},
        'contents': {'type': 'string'},
        'is_active': {'type': 'boolean'},
        'is_bought': {'type': 'boolean'}
    }


class ProductItemListController(BaseListController):
    resource_fields = resource_fields_
    model = ProductItem
    name = 'ProductItem'
    parser = parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Список экземпляров продуктов (купонов)', description='-',
                      schema=ProductItemResponseModel)
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

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=201, schema=ProductItemResponseModel,
                      summary='Создать новый экземпляр продукта (купон)', description='-')
    @swagger.reqparser(name='ProductItemCreateModel', parser=parser)
    def post(self):
        return super().post_()


class ProductItemController(BaseController):
    resource_fields = resource_fields_
    model = ProductItem
    name = 'ProductItem'
    parser = parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Экземпляр продукта (купона)', description='-',
                      schema=ProductItemResponseModel)
    def get(self, product_item_id):
        return super().get_(product_item_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=200, summary='Обнвоить экземпляр продукта (купона)', description='-',
                      schema=ProductItemResponseModel)
    @swagger.reqparser(name='ProductItemPutModel', parser=parser)
    def put(self, product_item_id):
        updates = self.parser.parse_args()
        err, obj = self.update_obj(product_item_id, updates)
        if err:
            return err
        if not obj:
            return not_found(self.name, product_item_id)
        if obj.user is not None:
            return {'error': 'can\' put, because product already bought'}, 400
        return marshal(obj, self.resource_fields)
