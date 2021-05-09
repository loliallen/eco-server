from pathlib import Path

from flask_restful import fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import (
    BaseListController, BaseController
)
from src.models.filter.FilterModel import Filter


class FilterResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'var_name': {'type': 'string'},
        'key_words': {'type': 'array', 'items': {'type': 'string'}},
        'bad_words': {'type': 'array', 'items': {'type': 'string'}},
        'coins_per_unit': {'type': 'integer'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'var_name': fields.String,
    'key_words': fields.List(fields.String),
    'bad_words': fields.List(fields.String),
    "coins_per_unit": fields.Float
}


class FilterControllerList(BaseListController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    img_field = 'image'
    img_path = Path('./src/statics/filters')

    @swagger.tags('Filters')
    @swagger.response(response_code=200, summary='Список фильтров', description='-', schema=FilterResponseModel)
    def get(self):
        return super().get_()


class FilterController(BaseController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'

    @swagger.tags('Filters')
    @swagger.response(response_code=200, summary='Фильтр', description='-', schema=FilterResponseModel)
    def get(self, filter_id):
        return super().get_(filter_id)
