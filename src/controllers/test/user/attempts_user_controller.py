from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.config import Configuration
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.QuestionModel import Question, QUESTION_TYPE_CHOICES
from src.models.test.Test import Test
from src.models.test.UsersAttemtps import UserAttempts
from src.models.user.UserModel import User

resource_attempt_fields = {
    'id': fields.String,
    'test_id': fields.String(attribute='test.id'),
    'test_name': fields.String(attribute='test.test_name'),
    'points': fields.Integer,
    'points_threshold': fields.Integer(attribute='test.points_to_success'),
    'is_success': fields.Boolean,
    'is_closed': fields.Boolean,
    'datetime_opened': fields.DateTime('iso8601'),
    'datetime_closed': fields.DateTime('iso8601'),
}


class UserAttemptResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'id попытки'},
        'test_id': {'type': 'string', 'description': 'id теста'},
        'test_name': {'type': 'string', 'description': 'Имя теста'},
        'points': {'type': 'integer', 'description': 'Количество набранных баллов'},
        'points_threshold': {'type': 'integer', 'description': 'Количество баллов для успешного прохождения'},
        'is_success': {'type': 'boolean', 'description': 'Успешность попытки'},
        'image': {'type': 'string', 'description': 'Ссылка на изображение'}
    }


resource_questions_fields = {
    'question_id': fields.String(attribute='id'),
    'question': fields.String,
    'question_type': fields.String,
    'answers_variants': fields.List(fields.String),
    'point_for_answer': fields.Integer,
    'image': custom_fields.ImageLink,
}


class QuestionResponseModel(Schema):
    properties = {
        'question_id': {'type': 'string', 'description': 'id вопроса'},
        'question': {'type': 'string', 'description': 'Вопрос'},
        'question_type': {'type': 'string', 'description': 'Тип вопроса', 'choices': QUESTION_TYPE_CHOICES},
        'answers_variants': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Варианты ответа'},
        'point_for_answer': {'type': 'integer', 'description': 'Количество баллов за ответ'}
    }


class AttemptCreateResponseModel(Schema):
    properties = {
        **UserAttemptResponseModel.properties,
        'questions': {'type': 'array', 'items': QuestionResponseModel, 'description': 'Оставшиеся вопросы'}
    }


class UserAttemptsListController(BaseListController):
    resource_fields = resource_attempt_fields
    model = UserAttempts
    name = 'UserAttempt'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Список попыток', description='-',
                      schema=UserAttemptResponseModel)
    def get(self):
        user = User.objects.filter(username=get_jwt_identity()).first()
        return super().get_(user=user)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.reorder_with(response_code=201, schema=AttemptCreateResponseModel,
                          summary='Создать новую попытку',
                          description='Если попытка уже была создана и не завершена - '
                                      'вернется старая попытка с оставшимися вопросами')
    def post(self):
        user = User.objects.filter(username=get_jwt_identity()).first()

        active_attempt = UserAttempts.objects.filter(user=user, is_closed=False).first()
        if active_attempt:
            already_answered_ids = [i.id for i in active_attempt.already_answered]
            tests_questions = Question.objects.filter(test=active_attempt.test,
                                                      id__nin=already_answered_ids).all()
            return {
                **marshal(active_attempt, resource_attempt_fields),
                'questions': marshal(list(tests_questions), resource_questions_fields)
            }

        last_attempts = UserAttempts.objects.filter(
            user=user,
            datetime_closed__gt=datetime.utcnow() - Configuration.TEST_FREEZE_TIME
        )
        available_test = Test.objects.filter(
            id__nin=[attempt.test.id for attempt in last_attempts],
            coins_to_unlock__lte=user.freeze_eco_coins
        ).first()

        if available_test is None:
            return {"error": "Available tests not found"}, 404

        attempt = UserAttempts.create_(user=user.id, test=available_test,
                                       datetime_opened=datetime.utcnow())
        tests_questions = Question.objects.filter(test=available_test).all()
        return {
            **marshal(attempt, resource_attempt_fields),
            'questions': marshal(list(tests_questions), resource_questions_fields)
        }


class UserAttemptsController(BaseController):
    resource_fields = resource_attempt_fields
    model = UserAttempts
    name = 'UserAttempt'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=200, summary='Попытка', description='-',
                      schema=UserAttemptResponseModel)
    def get(self, attempt_id):
        return super().get_(attempt_id)
