import datetime

from flask_restful import reqparse, Resource, fields
from flask_restful_swagger_3 import swagger, Schema

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
            return {'status': 'success'}, 200
        else:
            return {'message': 'Not valid code'}, 400
