import datetime

from flask_babel import lazy_gettext as _
from flask_restful import reqparse, Resource, fields
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, Status, ActionType
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help=_('Email'))
post_parser.add_argument('code', type=str, required=True, help=_('Check code from letter'))


class ConfirmResponseModel(Schema):
    properties = {
        'access_token': {'type': 'string'},
    }


resource_fields_ = {
    'access_token': fields.String
}


class ConfirmController(Resource):

    @swagger.tags('User')
    @swagger.response(response_code=201, schema=ConfirmResponseModel, summary='Подтвердить почту',
                      description='-')
    @swagger.reqparser(name='ConfirmModel', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        user = User.objects.filter(username=args['username']).first()
        if user is None:
            return {'error': _('User not found')}, 404
        if user.confirmed:
            return {'error': _('Account already confirmed. Please login.')}, 400
        if str(user.code) != args['code']:
            return {'message': _('Not valid code')}, 400

        user.update(confirmed=True, confirmed_on=datetime.datetime.utcnow())
        if user.invite_by_user is not None:
            # добавляем экокоины пользователю за приглашение
            AdmissionTransaction.create_and_pay_for_user(
                action_type=ActionType.invite.value,  # invite
                action=user,  # id действия в данном случае это id пользователя, который зарегался
                status=Status.confirmed.value,
                user=user.invite_by_user.id,  # это действие должно отображаться у пригласившего
                eco_coins=Configuration.ECO_COINS_BY_INVITE
            )
        return {'status': 'success'}, 200
