from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema, Resource

from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', type=str, required=True, help='Почта пользователя')
post_parser.add_argument('password', type=str, required=True, help='Пароль пользователя')


class UserInfoResponseModel(Schema):
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


class UserInfoController(Resource):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('User')
    @swagger.response(response_code=200, schema=UserInfoResponseModel, summary='Информация о пользователе',
                      description='-')
    def get(self):
        user = User.objects.filter(username=get_jwt_identity()).first()
        return marshal(user, resource_fields_)
