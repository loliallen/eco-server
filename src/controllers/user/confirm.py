import datetime

from flask_restful import reqparse, Resource, fields
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help='Почта пользователя')
post_parser.add_argument('code', type=str, required=True, help='Код из письма')


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
            return {'error': 'user not found'}, 404
        if user.confirmed:
            return {'error': 'Account already confirmed. Please login.'}, 400
        if str(user.code) == args['code']:
            user.update(confirmed=True, confirmed_on=datetime.datetime.utcnow())
            if user.invite_by_user is not None:
                # добавляем экокоины пользователю за приглашение
                AdmissionTransaction.create_and_pay_for_user(
                    action_type='i',
                    action=user,
                    user=user.invite_by_user.id,
                    eco_coins=Configuration.ECO_COINS_BY_INVITE
                )
            return {'status': 'success'}, 200
        else:
            return {'message': 'Not valid code'}, 400