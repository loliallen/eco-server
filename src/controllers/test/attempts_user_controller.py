from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.QuestionModel import Question
from src.models.test.Test import Test
from src.models.test.UsersAttemtps import UserAttempts
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('answers', type=dict, action='append', required=True, help='Ответы на тест')

resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='user.id'),
    'user_name': fields.String(attribute='user.name'),
    'test_id': fields.String(attribute='test.id'),
    'test_name': fields.String(attribute='test.test_name'),
    'points': fields.Integer,
    'points_threashold': fields.Integer(attribute='test.points_to_success'),
    'is_success': fields.Boolean,
}


class UserAttemptResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'user_name': {'type': 'string'},
        'test_id': {'type': 'string'},
        'test_name': {'type': 'string'},
        'is_success': {'type': 'boolean'}
    }


class UserAttemptCreateModel(Schema):
    properties = {
        'answers': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'question_id': {
                        'type': 'string',
                        'description': 'Id вопроса'
                    },
                    'answer': {
                        'type': 'string',
                        'description': 'Ответ на вопрос'
                    }
                }
            }
        }
    }


class UserAttemptsListController(BaseListController):
    resource_fields = resource_fields_
    model = UserAttempts
    name = 'UserAttempt'
    parser = post_parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список попыток', description='-',
                      schema=UserAttemptResponseModel)
    def get(self, test_id):
        user = User.objects.filter(username=get_jwt_identity()).first()
        return super().get_(test=test_id, user=user.id)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=201, schema=UserAttemptResponseModel,
                      summary='Отправить попытку', description='Отправить ответы на вопросы одного теста')
    @swagger.expected(UserAttemptCreateModel, required=True)
    # @swagger.reqparser(name='UserAttemptCreateModel', parser=post_parser)
    def post(self, test_id):
        args = post_parser.parse_args()
        answers = {i['question_id']: i['answer'] for i in args['answers']}
        test = Test.find_by_id_(_id=test_id)
        questions = Question.objects(test=test_id).all()
        points = 0
        for question in questions:
            if answers.get(str(question.id)) is None:
                return {'error': 'не на все вопросы даны ответы'}, 400
            if answers[str(question.id)] == question.correct_answer:
                points += question.point_for_answer
        user = User.objects.filter(username=get_jwt_identity()).first()
        obj, error = self._create_obj(test=test_id, user=user,
                                      points=points,
                                      is_success=points >= test.points_to_success)
        if error:
            return error
        return marshal(obj, self.resource_fields)


class UserAttemptsController(BaseController):
    resource_fields = resource_fields_
    model = UserAttempts
    name = 'UserAttempt'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Попытка', description='-',
                      schema=UserAttemptResponseModel)
    def get(self, test_id, attempt_id):
        return super().get_(attempt_id, test=test_id)
