from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.QuestionModel import Question, QUESTION_TYPE_CHOICES

parser = reqparse.RequestParser()
parser.add_argument('question', type=str, required=True, help='название вопроса')
parser.add_argument('question_type', type=str, required=True, choices=QUESTION_TYPE_CHOICES, help='Тип вопроса')
parser.add_argument('answers_variants', type=str, action='append', required=True, help='Варианты ответа')
parser.add_argument('correct_answer', type=str, required=True, help='Правильный ответ')
parser.add_argument('description', type=str, required=True, help='Пояснение')
parser.add_argument('point_for_answer', type=int, help='Количество баллов за ответ')


resource_fields_ = {
    'id': fields.String,
    'test': fields.String(attribute='test.id'),
    'question': fields.String,
    'question_type': fields.String,
    'answers_variants': fields.List(fields.String),
    'correct_answer': fields.String,
    'description': fields.String,
    'point_for_answer': fields.Integer
}


class QuestionResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'test': {'type': 'string'},
        'question': {'type': 'string'},
        'question_type': {'type': 'string', 'choices': QUESTION_TYPE_CHOICES},
        'answers_variants': {'type': 'array', 'items': {'type': 'string'}},
        'correct_answer': {'type': 'string'},
        'description':  {'type': 'string'},
        'point_for_answer': {'type': 'integer'}
    }


class QuestionListController(BaseListController):
    resource_fields = resource_fields_
    model = Question
    name = 'Question'
    parser = parser

    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список вопросов', description='-',
                      schema=QuestionResponseModel)
    def get(self, test_id):
        return super().get_(test=test_id)

    @swagger.tags('Tests')
    @swagger.response(response_code=201, schema=QuestionResponseModel,
                      summary='Создать новый вопрос', description='-')
    @swagger.reqparser(name='QuestionCreateModel', parser=parser)
    def post(self, test_id):
        return super().post_(test=test_id)

    def get_fields(self):
        return self.parser.parse_args()


class QuestionController(BaseController):
    resource_fields = resource_fields_
    model = Question
    name = 'Question'
    parser = parser

    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Вопрос', description='-',
                      schema=QuestionResponseModel)
    def get(self, test_id, question_id):
        return super().get_(question_id, test=test_id)

    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Обновить вопрос', description='-',
                      schema=QuestionResponseModel)
    @swagger.reqparser(name='QuestionPutModel', parser=parser)
    def put(self, test_id, question_id):
        return super().put_(question_id, test=test_id)

    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Удалить вопрос', description='-',
                      schema=QuestionResponseModel)
    def delete(self, test_id, question_id):
        return super().delete_(question_id, test=test_id)
