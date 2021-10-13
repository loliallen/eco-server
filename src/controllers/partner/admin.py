from flask_restful import reqparse, fields
from flask_babel import lazy_gettext as _
from flask_restful_swagger_3 import swagger, Schema

from models.utils.enums import Status
from src.models.user.UserModel import User
from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController, not_found
from src.models.partner.PartnerModel import Partner
from src.utils.roles import jwt_reqired_backoffice, Roles

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True)
post_parser.add_argument('user', type=str, required=True)
post_parser.add_argument('request_message', type=str, required=False)
post_parser.add_argument('status', type=str, choices=(Status.confirmed.value,
                                                      Status.dismissed.value), required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('name', type=str, required=True)
put_parser.add_argument('status', type=str, choices=(Status.confirmed.value,
                                                     Status.dismissed.value), required=True)


class PartnerAdminResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'points': {'type': 'object'},
        'products': {'type': 'object'},
        'status': {'type': 'string'},
        'request_message': {'type': 'string'},
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'user': fields.String(attribute='user.id'),
    'request_message': fields.String,
    'status': fields.String,
    'points': custom_fields.Dict,
    'products': custom_fields.Dict,
}


class PartnerListController(BaseListController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    parser = post_parser

    @jwt_reqired_backoffice('partner', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=200, summary='Список партнеров', description='-', schema=PartnerAdminResponseModel)
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        admin = User.get_user_from_request()
        if Roles(admin.role) == Roles.partner:
            args['user'] = admin
            args['status'] = Status.confirmed.value
        return super().get_(paginate_=True, **args)

    @jwt_reqired_backoffice('partner', 'create')
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=201, schema=PartnerAdminResponseModel, summary='Создать нового партнера',
                      description='-')
    @swagger.reqparser(name='PartnerAdminCreateModel', parser=post_parser)
    def post(self):
        args = post_parser.parse_args()
        user = User.find_by_id_(args['user'])
        if Partner.objects.filter(user=user, status__in=[Status.idle.value,
                                                         Status.confirmed.value]).count() > 0:
            return {'error': _('User already create partner')}, 400
        # при апруве проставляем юзера как партнера
        if args['status'] == Status.confirmed.value:
            user.update(set__role=Roles.partner.value)
        # при отклонении проставляем, если юзер являлся партнером - понижаем его до юзера
        if args['status'] == Status.dismissed.value \
                and user.role == Roles.partner.value:
            user.update(set__role=Roles.user.value)
        return super().post_()


class PartnerController(BaseController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    parser = put_parser

    @jwt_reqired_backoffice('partner', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=200, summary='Партнер', description='-', schema=PartnerAdminResponseModel)
    def get(self, partner_id):
        kwargs = {}
        admin = User.get_user_from_request()
        if Roles(admin.role) == Roles.partner:
            kwargs['user'] = admin
        return super().get_(partner_id, **kwargs)

    @jwt_reqired_backoffice('partner', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.reqparser(name='PartnerAdminPutModel', parser=put_parser)
    @swagger.response(response_code=202, summary='Обноваить партнера', description='-', schema=PartnerAdminResponseModel)
    def put(self, partner_id):
        args = put_parser.parse_args()
        partner = Partner.find_by_id_(partner_id)
        if not partner:
            return not_found(self.name, partner_id)
        user = partner.user
        # при апруве проставляем юзера как партнера
        if args['status'] == Status.confirmed.value:
            user.update(set__role=Roles.partner.value)
        # при отклонении проставляем, если юзер являлся партнером - понижаем его до юзера
        if args['status'] == Status.dismissed.value and user.role == Roles.partner.value:
            user.update(set__role=Roles.user.value)
        return super().put_(partner_id)

    @jwt_reqired_backoffice('partner', 'delete')
    @swagger.security(JWT=[])
    @swagger.tags('Partners')
    @swagger.response(response_code=204, summary='Удалить партнера', description='-', schema=PartnerAdminResponseModel)
    def delete(self, partner_id):
        super().delete_(partner_id)
