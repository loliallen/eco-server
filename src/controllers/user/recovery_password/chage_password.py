from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseListController
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('password', type=str, required=True, help='Новый пароль')
post_parser.add_argument('password_repeat', type=str, required=True, help='Подтверждение пароля')


class ChangePasswordController(BaseListController):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('User/Recovery')
    @swagger.response(response_code=201, summary='Сменить пароль',
                      description='-')
    @swagger.reqparser(name='ChangePasswordModel', parser=post_parser)
    def post(self):
        if not get_jwt().get('is_recovery', False):
            return {'error': 'token is not recovery'}, 405
        args = post_parser.parse_args()
        user = User.get_user_from_request()
        if not user:
            return {'error': 'user not found'}, 404
        if args['password'] != args['password_repeat']:
            return {'error': 'passwords are not identical'}
        user.update(set__password=args['password'])
        return {'status': 'OK'}
