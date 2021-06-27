from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_img
from src.models.user.UserModel import User
from src.utils import custom_swagger

root = "users"


class UserImageUploaderController(BaseController):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('User')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображения профиля', description='-')
    @custom_swagger.mark_files_request()
    def post(self):
        user = User.get_user_from_request()
        save_img(user, root)
        return {'status': 'ok'}, 201
