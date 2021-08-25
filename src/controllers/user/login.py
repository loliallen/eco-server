import datetime

from flask_babel import lazy_gettext as _
from flask_jwt_extended import create_access_token
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema, Resource

from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help=_('Email'))
post_parser.add_argument('password', type=str, required=True, help=_('Password'))


class LoginResponseModel(Schema):
    properties = {
        'access_token': {'type': 'string'},
    }


resource_fields_ = {
    'access_token': fields.String
}


class LoginController(Resource):

    @swagger.tags('User')
    @swagger.response(response_code=201, schema=LoginResponseModel, summary='Логин',
                      description='-')
    @swagger.reqparser(name='LoginModel', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        user = User.objects.filter(username=args['username']).first()
        if not user:
            return {'error': _('Wrong login or password')}, 404
        if not user.check_password(args['password']):
            return {'error': _('Wrong login or password')}, 403
        if not user.confirmed:
            return {'error': _('User not confirmed')}, 403
        user.update(set__last_login=datetime.datetime.utcnow)
        access_token = create_access_token(identity=args['username'])
        return marshal({'access_token': access_token}, resource_fields_)
