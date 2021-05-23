from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.Test import Test

parser = reqparse.RequestParser()
parser.add_argument('test_name', type=str, required=True, help='Название теста')
parser.add_argument('description', type=str, required=True, help='Описание')
parser.add_argument('coins_to_unlock', type=int, required=True, help='Количество коинов, которые разблокирует тест')
parser.add_argument('points_to_success', type=int, required=True, help='Количество баллов для успешного прохождения')


resource_fields_ = {
    'id': fields.String,
    'test_name': fields.String,
    'description': fields.String,
    'coins_to_unlock': fields.Integer,
    'points_to_success': fields.Integer,
}


class TestResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'test_name': {'type': 'string'},
        'description': {'type': 'string'},
        'coins_to_unlock': {'type': 'integer'},
        'points_to_success': {'type': 'integer'}
    }


class TestListController(BaseListController):
    resource_fields = resource_fields_
    model = Test
    name = 'Test'
    parser = parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список тестов', description='-',
                      schema=TestResponseModel)
    def get(self):
        return super().get_()


class TestController(BaseController):
    resource_fields = resource_fields_
    model = Test
    name = 'Test'
    parser = parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Test')
    @swagger.response(response_code=200, summary='Тест', description='-',
                      schema=TestResponseModel)
    def get(self, question_id):
        return super().get_(question_id)
