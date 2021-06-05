from ast import literal_eval
from pathlib import Path

from bson import ObjectId
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.recpoint.RecPointModel import RecPoint

get_parser = reqparse.RequestParser()
get_parser.add_argument('coords', type=literal_eval, required=False, location='args')
get_parser.add_argument('filters', type=literal_eval, required=False, location='args')
get_parser.add_argument('payback_type', type=str, required=False, location='args')


class RecPointResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id пункта приема'},
        'name': {'type': 'string', 'description': 'Название приема'},
        'partner': {'type': 'string', 'description': 'Id партнера'},
        'partner_name': {'type': 'string', 'description': 'Название партнера'},
        'payback_type': {'type': 'string', 'description': 'Тип оплаты'},
        'work_time': {'type': 'string', 'description': 'Время работы пункта приема'},
        'address': {'type': 'string', 'description': 'Адрес пункта приема'},
        'contacts': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Список контактов'},
        'accept_types': {'type': 'array', 'items': {'type': 'string'},
                         'description': 'Список принимаемых фильтров (типов ресурса)'},
        'coords': {'type': 'array', 'items': {'type': 'float'}, 'description': 'Координаты пункта'},
        'description': {'type': 'string', 'description': 'Описание пункта'},
        'getBonus': {'type': 'boolean', 'description': 'Выплачивает ли пункт приема экокоины'},
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
    'accept_types': fields.List(fields.String(attribute='name')),
    'coords': fields.List(fields.Float, attribute='coords.coordinates'),
    'description': fields.String,
    'getBonus': fields.Boolean(attribute=lambda x: getattr(x, 'getBonus', False)),
}


class RecPointListController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'

    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Список пунктов приема',
                      description='-')
    @swagger.parameter(_in='query', name='coords', description='Ограничивающий полгион',
                       example='[12, 23], [34, 34], [34, 45]', schema={'type': 'string'})
    @swagger.parameter(_in='query', name='filters', description='Тип принимаемого фильтра (вида отхода)',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='payback_type', description='Тип оплаты',
                       example='free', schema={'type': 'string'})
    def get(self):
        args = get_parser.parse_args()
        points = RecPoint.read_(**args)
        return marshal(list(points), resource_fields_)


class RecPointController(BaseController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'

    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Пункт приема',
                      description='-')
    def get(self, rec_point_id):
        return super().get_(rec_point_id)
