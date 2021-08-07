from flask_restful import fields, reqparse
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.UsersAttemtps import UserAttempts
from src.utils.roles import jwt_reqired_backoffice


get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')
get_parser.add_argument('test', type=str, required=False, location='args')
get_parser.add_argument('user', type=str, required=False, location='args')


resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='user.id'),
    'user_name': fields.String(attribute='user.name'),
    'test_id': fields.String(attribute='test.id'),
    'test_name': fields.String(attribute='test.test_name'),
    'points': fields.Integer,
    'points_threshold': fields.Integer(attribute='test.points_to_success'),
    'datetime_opened': fields.DateTime('iso8601'),
    'datetime_closed': fields.DateTime('iso8601'),
    'is_success': fields.Boolean,
    'is_closed': fields.Boolean,
}


class AdminAttemptResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'user_name': {'type': 'string'},
        'test_id': {'type': 'string'},
        'test_name': {'type': 'string'},
        'points': {'type': 'integer'},
        'points_threshold': {'type': 'integer'},
        'is_success': {'type': 'boolean'}
    }


class AdminAttemptsListController(BaseListController):
    resource_fields = resource_fields_
    model = UserAttempts
    name = 'UserAttempt'

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список попыток', description='-',
                      schema=AdminAttemptResponseModel)
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        args = {k:v for k,v in args.items() if v is not None}
        return super().get_(paginate_=True, **args)


class AdminAttemptsController(BaseController):
    resource_fields = resource_fields_
    model = UserAttempts
    name = 'UserAttempt'

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Попытка', description='-',
                      schema=AdminAttemptResponseModel)
    def get(self, attempt_id):
        return super().get_(attempt_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Удалить попытку', description='-',
                      schema=AdminAttemptResponseModel)
    def delete(self, attempt_id):
        return super().delete_(attempt_id)
