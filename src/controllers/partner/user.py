from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.models.utils.enums import Status
from src.controllers.utils.BaseController import BaseListController
from src.models.partner.PartnerModel import Partner
from src.models.user.UserModel import User
from src.utils.roles import Roles

post_parser = reqparse.RequestParser()
post_parser.add_argument('request_message', type=str, required=False, help='Сообщение с запросом на создание')


class PartnerResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string', 'description': ''},
        'user': {'type': 'string',  'description': 'Id пользователя'},
        'request_message': {'type': 'string', 'description': 'Сообщение с запросом на создание'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'user': fields.String(attribute='user.id'),
    'request_message': fields.String,
}


class PartnerListController(BaseListController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    parser = post_parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=201, schema=PartnerResponseModel, summary='Оставить заявку на нового партнера',
                      description='-')
    @swagger.reqparser(name='PartnerCreateModel', parser=post_parser)
    def post(self):
        user = User.get_user_from_request()
        if Partner.objects.filter(user=user, status__in=[Status.idle.value,
                                                         Status.confirmed.value]).count() > 0:
            return {'error': _('You already create partner')}, 400
        if user.role != Roles.user.value:
            return {'error': _('Your role is not simple user')}, 400
        return super().post_(name='-', user=user.id)
