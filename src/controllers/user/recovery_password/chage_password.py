from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseListController
from src.controllers.utils.hash_password import generate_salt, hash_password
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('password', type=str, required=True, help=_('New password'))
post_parser.add_argument('password_repeat', type=str, required=True, help=_('New password confirm'))


class ChangePasswordController(BaseListController):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('User/Recovery')
    @swagger.response(response_code=201, summary='Сменить пароль',
                      description='-')
    @swagger.reqparser(name='ChangePasswordModel', parser=post_parser)
    def post(self):
        if not get_jwt().get('is_recovery', False):
            return {'error': _('Token is not recovery')}, 405
        args = post_parser.parse_args()
        user = User.get_user_from_request()
        if not user:
            return {'error': _('User not found')}, 404
        if args['password'] != args['password_repeat']:
            return {'error': _('Passwords are not identical')}
        salt = generate_salt()
        args['password'] = hash_password(args['password'], salt)
        user.update(set__password=args['password'], set__salt=salt)
        return {'status': 'ok'}, 200
