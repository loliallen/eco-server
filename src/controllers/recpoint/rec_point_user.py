from ast import literal_eval
from pathlib import Path

from bson import ObjectId
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
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'partner': {'type': 'string'},
        'partner_name': {'type': 'string'},
        'payback_type': {'type': 'string'},
        'work_time': {'type': 'object'},
        'contacts': {'type': 'array', 'items': {'type': 'string'}},
        'accept_types': {'type': 'array', 'items': {'type': 'string'}},
        'coords': {'type': 'array', 'items': {'type': 'float'}},
        'description': {'type': 'string'},
        'getBonus': {'type': 'boolean'},
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'partner': fields.String(attribute='partner.id'),
    'partner_name': fields.String(attribute='partner.name'),
    'payback_type': fields.String,
    'reception_type': fields.String,
    'work_time': custom_fields.Dict,
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

    @swagger.tags('RecPoints')
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

    @swagger.tags('RecPoints')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Пункт приема',
                      description='-')
    def get(self, rec_point_id):
        return super().get_(rec_point_id)

