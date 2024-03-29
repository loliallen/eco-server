from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse
from flask_restful_swagger_3 import swagger, Schema, Resource

from src.controllers.utils import fields as custom_fields
from src.models.user.UserModel import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, help='Имя пользователя')


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
        'role': {'type': 'string', 'description': 'Роль'},
        'attached_rec_point_id': {'type': 'string', 'description': 'Прикрепленный пункт приема (только для админов ПП)'},
        'image': {'type': 'string', 'description': 'Ссылка на изображение'},
    }


resource_fields_ = {
    'id': fields.String,
    'username': fields.String,
    'name': fields.String,
    'confirmed': fields.Boolean,
    'eco_coins': fields.Integer,
    'freeze_eco_coins': fields.Integer,
    'token': fields.String,
    'invite_code': fields.String(attribute='token'),
    'role': fields.String,
    'attached_rec_point_id': fields.String(attribute='attached_rec_point.id'),
    'image': custom_fields.ImageLink,
}


class UserInfoController(Resource):
    resource_fields = resource_fields_
    model = User
    name = 'User'
    parser = post_parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('User')
    @swagger.response(response_code=200, schema=UserInfoResponseModel, summary='Информация о пользователе',
                      description='-')
    def get(self):
        user = User.objects.filter(username=get_jwt_identity()).first()
        return marshal(user, resource_fields_)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('User')
    @swagger.response(response_code=200, schema=UserInfoResponseModel, summary='Обновить информацию о пользователе',
                      description='-')
    @swagger.reqparser(name='UserUpdateModel', parser=post_parser)
    def put(self):
        updates = self.parser.parse_args()
        user = User.get_user_from_request()
        user: User
        user.update(**updates)
        return marshal(user, resource_fields_)
