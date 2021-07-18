from ast import literal_eval

from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.controllers.utils.pagination import paginate
from src.controllers.utils.statistics_collector import collect_stat
from src.models.recpoint.RecPointModel import RecPoint, RECEPTION_TYPE_CHOICES, PAYBACK_TYPE_CHOICES
from src.models.utils.enums import Status

get_parser = reqparse.RequestParser()
get_parser.add_argument('filters', type=literal_eval, required=False, location='args')
get_parser.add_argument('payback_type', type=str, required=False, location='args')
get_parser.add_argument('reception_type', type=str, required=False, location='args')
get_parser.add_argument('position', type=literal_eval, required=True, location='args')
get_parser.add_argument('radius', type=int, required=True, location='args')
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


class RecPointResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id пункта приема'},
        'name': {'type': 'string', 'description': 'Название приема'},
        'partner': {'type': 'string', 'description': 'Id партнера'},
        'partner_name': {'type': 'string', 'description': 'Название партнера'},
        'payback_type': {'type': 'string', 'description': 'Тип оплаты', 'choices': PAYBACK_TYPE_CHOICES},
        'reception_type': {'type': 'string', 'description': 'Тип ', 'choices': RECEPTION_TYPE_CHOICES},
        'work_time': {'type': 'string', 'description': 'Время работы пункта приема'},
        'address': {'type': 'string', 'description': 'Адрес пункта приема'},
        'contacts': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Список контактов'},
        'accept_types': {'type': 'array', 'items': {'type': 'string'},
                         'description': 'Список принимаемых фильтров (типов ресурса)'},
        'coords': {'type': 'array', 'items': {'type': 'float'}, 'description': 'Координаты пункта'},
        'description': {'type': 'string', 'description': 'Описание пункта'},
        'getBonus': {'type': 'boolean', 'description': 'Выплачивает ли пункт приема экокоины'},
        'images': {'type': 'string', 'description': 'Ссылки на изображения'},
    }


resource_fields_reduced_ = {
    'id': fields.String,
    'name': fields.String,
    'payback_type': fields.String,
    'reception_type': fields.String,
    'accept_types_names': fields.List(fields.String(attribute='name'), attribute='accept_types'),
    'accept_types': fields.List(fields.String(attribute='id')),
    'coords': fields.List(fields.Float, attribute='coords.coordinates'),
}


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'partner': fields.String(attribute='partner.id'),
    'partner_name': fields.String(attribute='partner.name'),
    'payback_type': fields.String,
    'reception_type': fields.String,
    'work_time': custom_fields.Dict,
    'address': fields.String,
    'contacts': fields.List(fields.String),
    'accept_types_names': fields.List(fields.String(attribute='name'), attribute='accept_types'),
    'accept_types': fields.List(fields.String(attribute='id')),
    'coords': fields.List(fields.Float, attribute='coords.coordinates'),
    'description': fields.String,
    'getBonus': fields.Boolean(attribute=lambda x: getattr(x, 'getBonus', False)),
    "images": fields.List(custom_fields.ImageLink),
    "external_images": fields.List(fields.String),
    "approve_status": fields.String,
}


class RecPointListController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'

    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Список пунктов приема',
                      description='-')
    @swagger.parameter(_in='query', name='filters', description='Тип принимаемого фильтра (вида отхода)',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='payback_type', description='Тип оплаты',
                       schema={'type': 'string', 'enum': PAYBACK_TYPE_CHOICES})
    @swagger.parameter(_in='query', name='reception_type', description='Тип переработки',
                       schema={'type': 'string', 'enum': RECEPTION_TYPE_CHOICES})
    @swagger.parameter(_in='query', name='position', description='Координаты, относительно которых будут искаться ПП',
                       example='[55.799779, 49.1319283]', required=True, schema={'type': 'string'})
    @swagger.parameter(_in='query', name='radius', description='Радиус внутри которого будут искаться ПП',
                       example=50, required=True, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    # TODO: подумать, будем ли мы использовать эту статистику
    @collect_stat(get_parser)
    def get(self):
        args = get_parser.parse_args()
        if args.get('radius') > Configuration.MAX_RADIUS_REC_POINTS_SHOW:
            return {'error': 'too long radius'}, 400
        points = RecPoint.read(**args, approve_status=Status.confirmed.value)
        page = args.get('page')
        size = args.get('size')
        if page and size:
            return paginate(points, page, size, resource_fields_, select_related_depth=1)

        return marshal(points.select_related(max_depth=1), resource_fields_reduced_)


class RecPointController(BaseController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'

    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Пункт приема',
                      description='-')
    def get(self, rec_point_id):
        return super().get_(rec_point_id)
