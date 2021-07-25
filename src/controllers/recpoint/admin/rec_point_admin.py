from ast import literal_eval

from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.controllers.utils.pagination import paginate
from src.models.recpoint.RecPointModel import (
    RecPoint, PAYBACK_TYPE_CHOICES, RECEPTION_TYPE_CHOICES, DISTRICTS
)
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, ActionType
from src.models.user.UserModel import User
from src.models.utils.enums import STATUS_CHOICES
from src.utils.roles import jwt_reqired_backoffice, role_need, Roles

get_parser = reqparse.RequestParser()
get_parser.add_argument('filters', type=str, action='append', required=False, location='args')
get_parser.add_argument('payback_type', type=str, required=False, location='args')
get_parser.add_argument('reception_type', type=str, required=False, location='args')
get_parser.add_argument('position', type=str, action='append', required=False, location='args')
get_parser.add_argument('radius', type=int, required=False, location='args')
get_parser.add_argument('status', dest='approve_status', type=str, required=False, location='args')
get_parser.add_argument('page', type=int, required=False, default=1, location='args')
get_parser.add_argument('size', type=int, required=False, default=10, location='args')
get_parser.add_argument('id', dest='id__in', type=str, action='append', location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True)
post_parser.add_argument('address', type=str, required=True)
post_parser.add_argument('partner', type=str, required=False)
post_parser.add_argument('payback_type', type=str, required=False,
                         choices=PAYBACK_TYPE_CHOICES + (None,))
post_parser.add_argument('reception_type', type=str, required=False,
                         choices=RECEPTION_TYPE_CHOICES + (None,))
post_parser.add_argument('contacts', type=str, action='append', required=True)
post_parser.add_argument('work_time', type=dict, required=False)
post_parser.add_argument('accept_types', type=str, action='append', required=False)
post_parser.add_argument('coords', type=float, action='append', required=False)
post_parser.add_argument('description', type=str, required=False)
post_parser.add_argument('getBonus', type=bool, required=False)
post_parser.add_argument('external_images', type=str, action='append', required=False)
post_parser.add_argument('approve_status', type=str, choices=STATUS_CHOICES + (None,), required=False)
post_parser.add_argument('district', type=str, choices=DISTRICTS + (None,), required=False)


class RecPointResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'partner': {'type': 'string'},
        'partner_name': {'type': 'string'},
        'payback_type': {'type': 'string'},
        'work_time': {'type': 'object'},
        'address': {'type': 'string'},
        'contacts': {'type': 'array', 'items': {'type': 'string'}},
        'accept_types_names': {'type': 'array', 'items': {'type': 'string'}},
        'accept_types': {'type': 'array', 'items': {'type': 'string'}},
        'coords': {'type': 'array', 'items': {'type': 'float'}},
        'description': {'type': 'string'},
        'getBonus': {'type': 'boolean'},
        'district': {'type': 'string'},
        'images': {'type': 'string', 'description': 'Ссылки на изображения'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'partner': fields.String(attribute='partner.id'),
    'partner_name': fields.String(attribute='partner.name'),
    'payback_type': fields.String,
    'reception_type': fields.String,
    'address': fields.String,
    'work_time': custom_fields.Dict,
    'contacts': fields.List(fields.String),
    'accept_types_names': fields.List(fields.String(attribute='name'), attribute='accept_types'),
    'accept_types': fields.List(fields.String(attribute='id')),
    'coords': fields.List(fields.Float, attribute='coords.coordinates'),
    'description': fields.String,
    'getBonus': fields.Boolean(attribute=lambda x: getattr(x, 'getBonus', False)),
    "images": fields.List(custom_fields.ImageLink),
    "external_images": fields.List(fields.String),
    "approve_status": fields.String,
    "author": fields.String(attribute='author.id'),
    "change_by": fields.String(attribute='change_by.id'),
    "district": fields.String,
}


class RecPointListController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Список пунктов приема',
                      description='-')
    @swagger.parameter(_in='query', name='filters', description='Тип принимаемого фильтра (вида отхода)',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='payback_type', description='Тип оплаты',
                       example='free', schema={'type': 'string', 'enum': PAYBACK_TYPE_CHOICES})
    @swagger.parameter(_in='query', name='reception_type', description='Тип переработки',
                       example='free', schema={'type': 'string', 'enum': RECEPTION_TYPE_CHOICES})
    @swagger.parameter(_in='query', name='position', description='Координаты, относительно которых будут искаться ПП',
                       example='[55.799779, 49.1319283]', required=True, schema={'type': 'string'})
    @swagger.parameter(_in='query', name='radius', description='Радиус внутри которого будут искаться ПП',
                       example=10, required=True, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='status', description='Статус подтверждения',
                       required=False, schema={'type': 'string', 'enum': STATUS_CHOICES})
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        points = RecPoint.read(**args)
        page = args.get('page')
        size = args.get('size')

        return paginate(points, page, size, resource_fields_, select_related_depth=1)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Создать новый пункт приема',
                      description='-')
    @swagger.reqparser(name='RecPointCreateModel', parser=post_parser)
    def post(self):
        admin = User.get_user_from_request()
        return super().post_(author=admin)


class RecPointController(BaseController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Пункт приема',
                      description='-')
    def get(self, rec_point_id):
        return super().get_(rec_point_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Обновить пункт приема',
                      description='-')
    @swagger.reqparser(name='RecPointPutModel', parser=post_parser)
    def put(self, rec_point_id):
        updates = self.parser.parse_args()
        if updates['coords'] is None or updates['coords'] == [None]:
            updates.pop('coords')
        err, obj = self.update_obj(rec_point_id, updates)
        if err:
            return err
        return marshal(obj, resource_fields_)

    @jwt_reqired_backoffice()
    @role_need([Roles.super_admin])
    @swagger.security(JWT=[])
    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Удалить пункт приема',
                      description='-')
    def delete(self, rec_point_id):
        admission_transaction = AdmissionTransaction.objects.filter(
            action_type=ActionType.add_pp.value,
            action=rec_point_id.id).first()
        if admission_transaction is not None:
            admission_transaction.update(set__action=None)
        return super().delete_(rec_point_id)
