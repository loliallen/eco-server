from flask_jwt_extended import create_access_token
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.controllers.utils.BaseController import BaseListController
from src.models.user.UserModel import User
from src.models.user.UsersCodeNotify import UsersCodeNotify

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help='Почта пользователя')
post_parser.add_argument('code', type=str, required=True, help='Проверочный код')


class RecoveryTokenResponseModel(Schema):
    properties = {
        'recovery_token': {'type': 'string'},
    }


resource_fields_ = {
    'recovery_token': fields.String
}


class RecoveryTokenController(BaseListController):

    @swagger.tags('User/Recovery')
    @swagger.response(response_code=201, schema=RecoveryTokenResponseModel,
                      summary='Получить токен для смены пароля',
                      description=f'Время жизни токена для смены пароля '
                                  f'{Configuration.RECOVERY_TOKEN_EXPIRES.seconds / 60} минут(ы)')
    @swagger.reqparser(name='CheckCodeModel', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        user = User.objects.filter(username=args['username']).first()
        if not user:
            return {'error': 'user not found'}, 404
        notify = UsersCodeNotify.objects.filter(user=user, notify_type='recovery').first()
        if not notify:
            return {'error': 'check code not sent, or is deprecated'}
        if args['code'] != notify.code:
            return {'error': 'wrong check code'}
        notify.delete()
        token = create_access_token(
            identity=args['username'],
            expires_delta=Configuration.RECOVERY_TOKEN_EXPIRES,
            additional_claims={"is_recovery": True}
        )
        return marshal({'recovery_token': token}, resource_fields_)
