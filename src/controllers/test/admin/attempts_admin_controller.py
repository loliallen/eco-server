from flask_restful import fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.UsersAttemtps import UserAttempts

resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='user.id'),
    'user_name': fields.String(attribute='user.name'),
    'test_id': fields.String(attribute='test.id'),
    'test_name': fields.String(attribute='test.test_name'),
    'points': fields.Integer,
    'points_threshold': fields.Integer(attribute='test.points_to_success'),
    'is_success': fields.Boolean,
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

    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список попыток', description='-',
                      schema=AdminAttemptResponseModel)
    def get(self, test_id):
        return super().get_(test=test_id)


class AdminAttemptsController(BaseController):
    resource_fields = resource_fields_
    model = UserAttempts
    name = 'UserAttempt'

    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Попытка', description='-',
                      schema=AdminAttemptResponseModel)
    def get(self, test_id, attempt_id):
        return super().get_(attempt_id, test=test_id)
