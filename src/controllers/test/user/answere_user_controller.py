from datetime import datetime

from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController
from src.models.test.QuestionModel import Question
from src.models.test.UsersAttemtps import UserAttempts
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
    def post(self, attempt_id):
        attempt = UserAttempts.objects.filter(id=attempt_id).first()
        if not attempt:
            return {'error': _('Attempt not found')}, 404
        user = User.get_user_from_request()
        if attempt.user != user:
            return {'error': _('Permission denied')}, 405
        if attempt.is_closed:
            return {'error': _('Attempt is closed')}, 400

        args = post_parser.parse_args()
        all_test_questions = Question.objects.filter(test=attempt.test).all()
        if args['question_id'] not in [str(i.id) for i in all_test_questions]:
            return {'error': _('This question not in test')}, 400
        if args['question_id'] in attempt.already_answered:
            return {'error': _('This question already answered')}, 400
        question = Question.find_by_id_(_id=args['question_id'])
        attempt.already_answered.append(question)
        answer_is_right = bool(question.correct_answer == args['answer'])
        if answer_is_right:
            attempt.points += question.point_for_answer
        if len(attempt.already_answered) == len(all_test_questions):
            attempt.is_closed = True
            attempt.is_success = bool(attempt.points >= attempt.test.points_to_success)
            attempt.datetime_closed = datetime.now()
            if attempt.is_success:
                # разблокируем пользователю экокоины
                with user.lock() as user:
                    user.update(inc__freeze_eco_coins=-attempt.test.coins_to_unlock,
                                inc__eco_coins=attempt.test.coins_to_unlock)
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
                "points_to_success": attempt.test.points_to_success,
                "is_attempt_success": attempt.is_success
            })
        return answer
