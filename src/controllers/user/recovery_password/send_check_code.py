from flask import render_template
from flask_mail import Message
from flask_babel import lazy_gettext as _
from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.config import Configuration
from src.controllers.utils.BaseController import BaseListController
from src.models.user.UserModel import User
from src.models.user.UsersCodeNotify import UsersCodeNotify
from src.send_email import send_email
from src.utils.generator import generate_code

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help=_('Email'))


class RecoverySendCheckCodeController(BaseListController):

    @swagger.tags('User/Recovery')
    @swagger.response(response_code=201, summary='Отправить проверочный код',
                      description='Время жизни проверочного кода 2 минуты')
    @swagger.reqparser(name='SendCheckCodeModel', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        user = User.objects.filter(username=args['username']).first()
        if not user:
            return {'error': _('User not found')}, 404
        notify = UsersCodeNotify.objects.filter(user=user, notify_type='recovery').first()
        if notify:
            return {'error': _('Check code already sent, please '
                               'wait %(value)s seconds to send check code again.',
                               Configuration.RECOVERY_TOKEN_EXPIRES)}

        code = str(generate_code())
        UsersCodeNotify.create_(
            user=user,
            code=code,
            notify_type='recovery'
        )

        print(code)
        html = render_template('reset.html', code=code, name=user.name)
        subject = "Password recovery for Eco Application"
        message = Message(subject=subject, html=html, recipients=[user.username])
        send_email(message)

        return {'status': 'OK'}
