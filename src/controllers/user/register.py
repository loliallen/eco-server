from pathlib import Path

import werkzeug.datastructures
from flask import render_template
from flask_login import login_user
from flask_mail import Message
from flask_restful import reqparse, fields, marshal
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController
from src.models.user.UserModel import User
from src.send_email import send_email

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, help='Имя пользователя')
post_parser.add_argument('username', type=str, required=True, help='Почта пользователя')
post_parser.add_argument('password', type=str, required=True, help='Пароль пользователя')

post_parser_img = post_parser.copy()
post_parser_img.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')


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
    resource_fields = resource_fields_
    model = User
    name = 'User'
    parser = post_parser_img
    img_field = 'image'
    img_path = Path('./src/statics/users')

    @swagger.tags('User')
    @swagger.response(response_code=201, schema=RegisterResponseModel, summary='Зарегистрироваться',
                      description='-')
    @swagger.reqparser(name='RegisterCreateModel', parser=post_parser)
    def post(self):
        args = post_parser_img.parse_args()
        user, error = self._create_obj(**args)
        if error:
            return error
        code = user.code
        print(code)
        html = render_template('email.html', code=code)
        subject = "Please confirm your email"
        message = Message(subject=subject, html=html, recipients=[user.username])
        send_email(message)

        return marshal(user, resource_fields_)
