from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.Test import Test


resource_fields_ = {
    'id': fields.String,
    'test_name': fields.String,
    'description': fields.String,
    'coins_to_unlock': fields.Integer,
    'points_to_success': fields.Integer,
}


class TestResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'id теста'},
        'test_name': {'type': 'string', 'description': 'Имя теста'},
        'description': {'type': 'string', 'description': 'Описание теста'},
        'coins_to_unlock': {'type': 'integer', 'description': 'Кол-во разблокируемых экокоинов'},
        'points_to_success': {'type': 'integer', 'description': 'Кол-во баллов для успешного прохождения'}
    }


class TestListController(BaseListController):
    resource_fields = resource_fields_
    model = Test
    name = 'Test'

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

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Тест', description='-',
                      schema=TestResponseModel)
    def get(self, question_id):
        return super().get_(question_id)
