from flask_babel import lazy_gettext as _
from flask_jwt_extended import create_access_token
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema, Resource

from src.controllers.utils import fields as custom_fields
from src.config import Configuration
from src.models.user.UserModel import User
from src.utils.roles import Roles, BACKOFFICE_ACCESS_ROLES

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help='Почта пользователя')
post_parser.add_argument('password', type=str, required=True, help='Пароль пользователя')


class LoginResponseModelAdmin(Schema):
    properties = {
        'access_token': {'type': 'string'},
    }


resource_fields_ = {
    'id': fields.String,
    'fullName': fields.String(attribute='name'),
    'avatar': custom_fields.ImageLink(attribute='image'),
    'role': fields.String,
    'access_schema': custom_fields.Dict
}


class LoginController(Resource):

    @swagger.tags('Auth')
    @swagger.response(response_code=201, schema=LoginResponseModelAdmin, summary='Логин',
                      description='-')
    @swagger.reqparser(name='LoginModelAdmin', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        user = User.objects.filter(username=args['username']).first()
        if not user:
            return {'error': _('Wrong login or password')}, 404
        if not user.check_password(args['password']):
            return {'error': _('Wrong login or password')}, 403
        if not user.confirmed:
            return {'error': _('User not confirmed')}, 403
        if Roles(user.role) not in BACKOFFICE_ACCESS_ROLES:
            return {'error': _('You has not permission to admin api')}, 403
        access_token = create_access_token(
            identity=args['username'],
            expires_delta=Configuration.JWT_ADMIN_ACCESS_TOKEN_EXPIRES,
            additional_claims={"backoffice": True}
        )
        return {
            'access_token': access_token,
            'auth': marshal(user, resource_fields_),
        }
