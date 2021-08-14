from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_img
from src.models.test.QuestionModel import Question
from src.utils import custom_swagger
from src.utils.roles import jwt_reqired_backoffice

root = "question"


class QuestionImageUploaderController(BaseController):
    
    @jwt_reqired_backoffice('question', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Tests')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображение вопроса', description='-')
    @custom_swagger.mark_files_request()
    def post(self, question_id):
        question = Question.find_by_id_(question_id)
        if question is None:
            return {'error': f'Question not found'}, 404
        save_img(question, root)
        return {'status': 'ok'}, 201
