from pathlib import Path

from flask_restful import fields
from flask_restful_swagger_3 import swagger, Schema

import src.controllers.utils.fields as custom_fields
from src.controllers.utils.BaseController import (
    BaseListController, BaseController
)
from src.models.filter.FilterModel import Filter


class FilterResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id фильтра'},
        'name': {'type': 'string', 'description': 'Название фильтра'},
        'var_name': {'type': 'string', 'description': 'Код фильтра'},
        'key_words': {'type': 'array', 'items': {'type': 'string'},
                      'description': 'Список слов, используемых для поиска этого фильтра'},
        'bad_words': {'type': 'array', 'items': {'type': 'string'},
                      'description': 'Список слов, не используемых для поиска этого фильтра'},
        'coins_per_unit': {'type': 'integer',
                           'description': 'Количество коинов за единицу сданного типа ресурса'},
        'image': {'type': 'string',
                  'description': 'Ссылка на изображение'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'var_name': fields.String,
    'key_words': fields.List(fields.String),
    'bad_words': fields.List(fields.String),
    "coins_per_unit": fields.Float,
    "image": custom_fields.ImageLink,
}


class FilterControllerList(BaseListController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    img_field = 'image'
    img_path = Path('./src/statics/filters')

    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=200, summary='Список фильтров (Типов ресурса)',
                      description='-', schema=FilterResponseModel)
    def get(self):
        return super().get_(visible=True)


class FilterController(BaseController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'

    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=200, summary='Фильтр (Тип ресурса)',
                      description='-', schema=FilterResponseModel)
    def get(self, filter_id):
        return super().get_(filter_id, visible=True)
