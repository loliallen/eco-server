from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.test.QuestionModel import Question
from src.models.test.Test import Test
from src.models.test.UsersAttemtps import UserAttempts
from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('question_id', type=str, required=True, help='Id вопроса')
post_parser.add_argument('answer', type=str, required=True, help='Ответ')


class UserAnswerResponseModel(Schema):
    properties = {
        "answer_status": {'type': 'string', "description": "Статус ответа на вопрос (правильный/неправильный)"},
        "correct_answer": {'type': 'string', "description": "Правильный ответ"},
        "your_answer": {'type': 'string', "description": "Ответ пользователя"},
        "description": {'type': 'string', "description": "Пояснение к правильному ответу"},
        "current_points": {'type': 'string', "description": "Количество набранных баллов"},
        "points_to_success": {'type': 'string',
                              "description": "Кол-во баллов для успешного прохождения теста "
                                             "(после отправки последнего вопроса)"},
        "is_attempt_success": {'type': 'string',
                               "description": "Успешность попытки (после отправки последнего вопроса)"},
    }


class UserAnswerController(BaseListController):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.reqparser('UserAnswerModel', post_parser)
    @swagger.response(response_code=201, schema=UserAnswerResponseModel,
                      summary='Отправить ответ', description='Отправить ответы на вопрос')
    def post(self, test_id, attempt_id):

        test = Test.find_by_id_(_id=test_id)
        if test is None:
            return {'error': 'test not found'}, 404
        attempt = UserAttempts.objects.filter(id=attempt_id, test=test).first()
        if not attempt:
            return {'error': 'attempt not found'}, 404
        user = User.get_user_from_request()
        if attempt.user != user:
            return {'error': 'permission denied'}, 405
        if attempt.is_closed:
            return {'error': 'attempt is closed'}, 400

        args = post_parser.parse_args()
        all_test_questions = Question.objects.filter(test=test).all()
        if args['question_id'] not in [str(i.id) for i in all_test_questions]:
            return {'error': 'this question not in test'}, 400
        if args['question_id'] in attempt.already_answered:
            return {'error': 'this question already answered'}, 400
        question = Question.find_by_id_(_id=args['question_id'])
        attempt.already_answered.append(question)
        answer_is_right = bool(question.correct_answer == args['answer'])
        if answer_is_right:
            attempt.points += question.point_for_answer
        if len(attempt.already_answered) == len(all_test_questions):
            attempt.is_closed = True
            attempt.is_success = bool(attempt.points >= test.points_to_success)
            attempt.datetime_closed = datetime.now()
            # разблокируем пользователю экокоины
            with user.lock() as user:
                user.update(inc__freeze_eco_coins=-test.coins_to_unlock, inc__eco_coins=test.coins_to_unlock)
        attempt.save()
        answer = {
            "answer_status": answer_is_right,
            "correct_answer": question.correct_answer,
            "your_answer": args['answer'],
            "description": question.description,
            "current_points": attempt.points,
        }
        if attempt.is_closed:
            answer.update({
                "points_to_success": test.points_to_success,
                "is_attempt_success": attempt.is_success
            })
        return answer
