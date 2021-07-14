import datetime
from ast import literal_eval

from flask_restful import inputs
from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.controllers.utils import fields as custom_fields
from src.models.user.UserModel import User
from src.utils.roles import jwt_reqired_backoffice

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')
get_parser.add_argument('id', dest='id__in', type=str, action='append', location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True)
post_parser.add_argument('username', type=str, required=True)
post_parser.add_argument('confirmed', type=bool, required=True)
post_parser.add_argument('eco_coins', type=int, required=True)
post_parser.add_argument('freeze_eco_coins', type=int, required=True)
post_parser.add_argument('role', type=str, required=False)
post_parser.add_argument('token', type=str, required=True)
datetime_ = inputs.datetime_from_iso8601
datetime_.swagger_type = 'datetime'
post_parser.add_argument('confirmed_on', type=datetime_, required=False)
post_parser.add_argument('invite_by_user', type=str, required=False)


class UsersResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'username': {'type': 'string'},
        'confirmed': {'type': 'string'},
        'eco_coins': {'type': 'numeric'},
        'freeze_eco_coins': {'type': 'numeric'},
        'role': {'type': 'string'},
        'token': {'type': 'string'},
        'confirmed_on': {'type': 'datetime'},
        'invite_by_user': {'type': 'string'},
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'username': fields.String,
    'confirmed': fields.Boolean,
    'eco_coins': fields.Integer,
    'freeze_eco_coins': fields.Integer,
    'role': fields.String,
    'token': fields.String,
    'confirmed_on': fields.DateTime('iso8601'),
    'invite_by_user': fields.String(attribute='invite_by_user.id'),
    'image': custom_fields.ImageLink,
}


class UsersListController(BaseListController):
    resource_fields = resource_fields_
    model = User
    name = 'User'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Users')
    @swagger.response(response_code=201, schema=UsersResponseModel, summary='Список пользователей',
                      description='-')
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


class UsersController(BaseController):
    resource_fields = resource_fields_
    model = User
    name = 'User'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Users')
    @swagger.response(response_code=201, schema=UsersResponseModel, summary='Пункт приема',
                      description='-')
    def get(self, user_id):
        return super().get_(user_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Users')
    @swagger.response(response_code=201, schema=UsersResponseModel, summary='Обновить пользователя',
                      description='-')
    @swagger.reqparser(name='UserPutModel', parser=post_parser)
    def put(self, user_id):
        return super().put_(user_id)
