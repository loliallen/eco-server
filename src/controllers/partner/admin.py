from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.partner.PartnerModel import Partner
from src.utils.roles import jwt_reqired_backoffice

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True)


class PartnerResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'points': {'type': 'object'},
        'products': {'type': 'object'},
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'points': custom_fields.Dict,
    'products': custom_fields.Dict,
}


class PartnerListController(BaseListController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=200, summary='Список партнеров', description='-', schema=PartnerResponseModel)
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
    @swagger.tags('Partners')
    @swagger.response(response_code=201, schema=PartnerResponseModel, summary='Создать нового партнера',
                      description='-')
    @swagger.reqparser(name='PartnerCreateModel', parser=post_parser)
    def post(self):
        return super().post_()


class PartnerController(BaseController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    post_parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=200, summary='Партнер', description='-', schema=PartnerResponseModel)
    def get(self, partner_id):
        return super().get_(partner_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=200, summary='Обноваить партнера', description='-', schema=PartnerResponseModel)
    def put(self, partner_id):
        return super().put_(partner_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=200, summary='Удалить партнера', description='-', schema=PartnerResponseModel)
    def delete(self, partner_id):
        super().delete_(partner_id)
