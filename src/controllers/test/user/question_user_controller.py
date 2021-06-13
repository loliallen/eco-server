from flask_jwt_extended import jwt_required
from flask_restful import fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.QuestionModel import Question

resource_fields_ = {
    'id': fields.String,
    'test': fields.String(attribute='test.id'),
    'question': fields.String,
    'question_type': fields.String,
    'answers_variants': fields.List(fields.String),
    'correct_answer': fields.String,
    'point_for_answer': fields.Integer
}


class QuestionTempResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'test': {'type': 'string'},
        'question': {'type': 'string'},
        'question_type': {'type': 'string'},
        'answers_variants': {'type': 'array', 'items': {'type': 'string'}},
        'correct_answer': {'type': 'string'},
        'point_for_answer': {'type': 'integer'}
    }


class QuestionListController(BaseListController):
    resource_fields = resource_fields_
    model = Question
    name = 'Question'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список вопросов (!!!роут будет удален)', description='-',
                      schema=QuestionTempResponseModel)
    def get(self, test_id):
        return super().get_(test=test_id)


class QuestionController(BaseController):
    resource_fields = resource_fields_
    model = Question
    name = 'Question'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Вопрос (!!!роут будет удален)', description='-',
                      schema=QuestionTempResponseModel)
    def get(self, test_id, question_id):
        return super().get_(question_id, test=test_id)
