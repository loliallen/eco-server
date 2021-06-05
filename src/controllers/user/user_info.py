from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal
from flask_restful_swagger_3 import swagger, Schema, Resource

from src.models.user.UserModel import User


class UserInfoResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id пользователя'},
        'username': {'type': 'string', 'description': 'Почта пользователя'},
        'name': {'type': 'string', 'description': 'Имя пользователя'},
        'confirmed': {'type': 'boolean', 'description': 'Статус подтверждения'},
        'eco_coins': {'type': 'integer', 'description': 'Количество эко-коинов'},
        'freeze_eco_coins': {'type': 'integer', 'description': 'Количество замороженных эко-коинов'},
        'token': {'type': 'string', 'description': 'Уникальный токен для генерации QR кода'},
        'invite_code': {'type': 'string', 'description': 'Код для приглашения друга'},
    }


resource_fields_ = {
    'id': fields.String,
    'username': fields.String,
    'name': fields.String,
    'confirmed': fields.Boolean,
    'eco_coins': fields.Integer,
    'freeze_eco_coins': fields.Integer,
    'token': fields.String,
    'invite_code': fields.String(attribute='token')
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
