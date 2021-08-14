from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_img
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.user.UserModel import User
from src.utils import custom_swagger
from src.utils.roles import jwt_reqired_backoffice

root = "users"


class UserImageUploaderController(BaseController):

    @jwt_reqired_backoffice('users', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображения для транзакции зачисления '
                              '(Только для админов пункта  приема)', description='-')
    @custom_swagger.mark_files_request(is_list=True)
    def post(self, user_id):
        user = User.find_by_id_(user_id)
        if user is None:
            return {'error': f'User not found'}, 404
        save_img(user, root)
        return {'status': 'ok'}, 201
