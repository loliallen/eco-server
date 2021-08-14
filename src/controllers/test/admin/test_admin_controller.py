from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.Test import Test
from src.utils.roles import jwt_reqired_backoffice

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')
get_parser.add_argument('id', dest='id__in', type=str, action='append', location='args')

parser = reqparse.RequestParser()
parser.add_argument('test_name', type=str, required=True, help='Название теста')
parser.add_argument('description', type=str, required=True, help='Описание')
parser.add_argument('coins_to_unlock', type=int, required=True, help='Количество коинов, которые разблокирует тест')
parser.add_argument('points_to_success', type=int, required=True, help='Количество баллов для успешного прохождения')
parser.add_argument('is_active', type=bool, required=False, help='Доступность теста')


resource_fields_ = {
    'id': fields.String,
    'test_name': fields.String,
    'description': fields.String,
    'coins_to_unlock': fields.Integer,
    'points_to_success': fields.Integer,
    'is_active': fields.Boolean,
}


class TestResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'test_name': {'type': 'string'},
        'description': {'type': 'string'},
        'coins_to_unlock': {'type': 'integer'},
        'points_to_success': {'type': 'integer'},
        'is_active': {'type': 'boolean'},
    }


class TestListController(BaseListController):
    resource_fields = resource_fields_
    model = Test
    name = 'Test'
    parser = parser

    @jwt_reqired_backoffice('test', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список тестов', description='-',
                      schema=TestResponseModel)
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

    @jwt_reqired_backoffice('test', 'create')
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=201, schema=TestResponseModel,
                      summary='Создать новый тест', description='-')
    @swagger.reqparser(name='TestCreateModel', parser=parser)
    def post(self):
        return super().post_()


class TestController(BaseController):
    resource_fields = resource_fields_
    model = Test
    name = 'Test'
    parser = parser

    @jwt_reqired_backoffice('test', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Тест', description='-',
                      schema=TestResponseModel)
    def get(self, test_id):
        return super().get_(test_id)

    @jwt_reqired_backoffice('test', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Обновить тест', description='-',
                      schema=TestResponseModel)
    @swagger.reqparser(name='TestPutModel', parser=parser)
    def put(self, test_id):
        return super().put_(test_id)

    @jwt_reqired_backoffice('test', 'delete')
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Удалить тест', description='-',
                      schema=TestResponseModel)
    def delete(self, test_id):
        return super().delete_(test_id)
