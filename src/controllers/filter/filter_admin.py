from pathlib import Path

from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.controllers.utils.BaseController import (
    BaseListController, BaseController
)
from src.models.filter.FilterModel import Filter

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, help='Название фильтра')
post_parser.add_argument('var_name', type=str, required=True, help='Код фильтра')
post_parser.add_argument('key_words', type=str, action='append', required=True,
                         help='Список слов, используемых для поиска этого фильтра')
post_parser.add_argument('bad_words', type=str, action='append', required=True,
                         help='Спиок слов, не используемых для поиска этого фильтра')
post_parser.add_argument('coins_per_unit', type=int, help='Количество коинов за единицу сданного типа ресурса')


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
                           'description': 'Количество коинов за единицу сданного типа ресурса'}
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'var_name': fields.String,
    'key_words': fields.List(fields.String),
    'bad_words': fields.List(fields.String),
    "coins_per_unit": fields.Float,
    "image": fields.String(attribute=lambda x: f'{Configuration.STATIC_URL}{x.image}' if x.image else None),
}


class FilterControllerList(BaseListController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = post_parser
    img_field = 'image'
    img_path = Path('./src/statics/filters')

    @swagger.tags('Filters')
    @swagger.response(response_code=200, summary='Список фильтров', description='-', schema=FilterResponseModel)
    def get(self):
        return super().get_()

    @swagger.tags('Filters')
    @swagger.response(response_code=201, schema=FilterResponseModel, summary='Создать новый фильтр')
    @swagger.reqparser(name='FilterCreateModel', parser=post_parser)
    def post(self):
        """Создать новый фильтр"""
        return super().post_()


class FilterController(BaseController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = post_parser

    @swagger.tags('Filters')
    @swagger.response(response_code=200, summary='Фильтр', description='-', schema=FilterResponseModel)
    def get(self, filter_id):
        return super().get_(filter_id)

    @swagger.tags('Filters')
    @swagger.response(response_code=204, summary='Обновить Фильтр', description='-', schema=FilterResponseModel)
    @swagger.reqparser(name='FilterPutModel', parser=post_parser)
    def put(self, filter_id):
        return super().put_(filter_id)

    @swagger.tags('Filters')
    @swagger.response(response_code=204, summary='Удалить фильтр', description='-', schema=FilterResponseModel)
    def delete(self, filter_id):
        return super().delete_(filter_id)
