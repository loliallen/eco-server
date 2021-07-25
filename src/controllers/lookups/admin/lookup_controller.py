from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import (
    BaseListController
)
from src.models.filter.FilterModel import Filter
from src.models.recpoint.RecPointModel import DISTRICTS
from src.utils.roles import jwt_reqired_backoffice

LOOKUP = ('filter', 'district')

get_parser = reqparse.RequestParser()
get_parser.add_argument('type', type=str, choices=LOOKUP, required=True, location='args')


class LookupsControllerList(BaseListController):
    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Lookups')
    @swagger.response(response_code=200, summary='Список значений', description='-')
    @swagger.parameter(_in='query', name='type',
                       description='Тип параметра',
                       required=True, schema={'type': 'string', 'enum': LOOKUP})
    def get(self):
        args = get_parser.parse_args()
        return {
            'filter': marshal(list(Filter.read_()), {'id': fields.String, 'name': fields.String}),
            'district': list(DISTRICTS),
        }[args['type']]
