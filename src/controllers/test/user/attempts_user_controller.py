from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema
from flask import request

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.QuestionModel import Question, QUESTION_TYPE_CHOICES
from src.models.test.Test import Test
from src.models.test.UsersAttemtps import UserAttempts
from src.models.user.UserModel import User
from src.config import Configuration

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
        'is_success': {'type': 'boolean', 'description': 'Успешность попытки'}
    }


resource_questions_fields = {
    'question_id': fields.String(attribute='id'),
    'question': fields.String,
    'question_type': fields.String,
    'answers_variants': fields.List(fields.String),
    'point_for_answer': fields.Integer,
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
    def get(self, test_id):
        user = User.objects.filter(username=get_jwt_identity()).first()
        return super().get_(test=test_id, user=user.id)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.reorder_with(response_code=201, schema=AttemptCreateResponseModel,
                          summary='Создать новую попытку',
                          description='Если попытка уже была создана и не завершена - '
                                      'вернется старая попытка с оставшимися вопросами')
    def post(self, test_id):
        test = Test.find_by_id_(_id=test_id)
        if test is None:
            return {"error": "Test not found"}, 404
        user = User.objects.filter(username=get_jwt_identity()).first()
        if user.freeze_eco_coins < test.coins_to_unlock:
            return {'error': 'yours freeze ecocoins less than test unlock'}, 400

        latest_attempt = UserAttempts.objects.filter(user=user.id).order_by('-datetime_opened').first()
        if latest_attempt:
            # если имеется незаконченная попытка  другого теста, то не начинаем новую
            if latest_attempt.test.id != test.id:
                if not latest_attempt.is_closed:
                    return {'error': 'yau can\'t to solve multiple test at the same time'}
            else:
                # если уже имеется незакрытая попытка этого же теста -
                # то возвращаем оставшиеся вопросы этой попытки
                if not latest_attempt.is_closed:
                    already_answered_ids = [i.id for i in latest_attempt.already_answered]
                    tests_questions = Question.objects.filter(test=test_id, id__nin=already_answered_ids).all()
                    return {
                        **marshal(latest_attempt, resource_attempt_fields),
                        'questions': marshal(list(tests_questions), resource_questions_fields)
                    }

                if datetime.now() < latest_attempt.datetime_opened + Configuration.TEST_FREEZE_TIME:
                    return {'error': 'not enough time has passed since the last attempt'}, 400

        attempt = UserAttempts.create_(user=user.id, test=test_id, datetime_opened=datetime.now())
        tests_questions = Question.objects.filter(test=test_id).all()
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
    def get(self, test_id, attempt_id):
        return super().get_(attempt_id, test=test_id)
