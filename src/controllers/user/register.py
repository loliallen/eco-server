from flask import render_template
from flask_babel import lazy_gettext as _
from flask_mail import Message
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import inputs
from src.controllers.utils.BaseController import BaseListController
from src.controllers.utils.hash_password import generate_salt, hash_password
from src.models.user.UserModel import User
from src.send_email import send_email

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=inputs.NotEmptyString(), required=True,
                         help=_('Username must be not empty'))
post_parser.add_argument('username', type=inputs.Email(), required=True,
                         help=_('Email must contains: mail addres, @, provider, doman (.com)'))
post_parser.add_argument('password', type=inputs.Password(), required=True,
                         help=_('Password must contains %(value)s', value=inputs.Password.help_msg))
post_parser.add_argument('invite_code', type=str, required=False, help='Код приглашения')


class RegisterResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'username': {'type': 'string'},
        'name': {'type': 'string'},
        'confirmed': {'type': 'boolean'},
        'eco_coins': {'type': 'integer'},
    }


resource_fields_ = {
    'id': fields.String,
    'username': fields.String,
    'name': fields.String,
    'confirmed': fields.Boolean,
    'eco_coins': fields.Integer
}


class RegisterController(BaseListController):
    model = User


    @swagger.tags('User')
    @swagger.response(response_code=201, schema=RegisterResponseModel, summary='Зарегистрироваться',
                      description='-')
    # @swagger.reqparser(name='RegisterCreateModel', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        invite_code = args.pop('invite_code')
        if invite_code:
            invite_user = User.objects.filter(token=invite_code).first()
            if invite_user is None:
                return {'error': 'invite user not found'}, 400
            args['invite_by_user'] = invite_user
        args['salt'] = generate_salt()
        args['password'] = hash_password(args['password'], args['salt'])
        user, error = self._create_obj(**args)
        if error:
            return error

        # TODO вынести это дело в фоновую таску
        code = user.code
        print(code)
        html = render_template('email.html', code=code)
        subject = "Please confirm your email"
        message = Message(subject=subject, html=html, recipients=[user.username])
        send_email(message)

        return marshal(user, resource_fields_)
