from flask_restful import reqparse, fields
from flask_restful.inputs import boolean
from flask_restful_swagger_3 import swagger, Schema

import src.controllers.utils.fields as custom_fields
from src.controllers.utils.BaseController import (
    BaseListController, BaseController
)
from src.models.filter.FilterModel import Filter
from src.utils.roles import jwt_reqired_backoffice

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')
get_parser.add_argument('id', dest='id__in', type=str, action='append', location='args')
get_parser.add_argument('visible', type=boolean, location='args')

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, help='Название фильтра')
post_parser.add_argument('var_name', type=str, required=True, help='Код фильтра')
post_parser.add_argument('key_words', type=str, action='append', required=True,
                         help='Список слов, используемых для поиска этого фильтра')
post_parser.add_argument('bad_words', type=str, action='append', required=True,
                         help='Спиок слов, не используемых для поиска этого фильтра')
post_parser.add_argument('coins_per_unit', type=int, help='Количество коинов за '
                                                          'единицу сданного типа ресурса')
post_parser.add_argument('visible', type=bool, help='Видимость типа ресурса')


class FilterResponseModelAdmin(Schema):
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
                  'description': 'Ссылка на изображение'},
        'visible': {'type': 'string', 'description': 'Видимость для пользователя'},
    }


resource_fields_ = {
    'id': fields.String,
    'name': fields.String,
    'var_name': fields.String,
    'key_words': fields.List(fields.String),
    'bad_words': fields.List(fields.String),
    "coins_per_unit": fields.Float,
    "image": custom_fields.ImageLink,
    "visible": fields.Boolean,
}


class FilterControllerList(BaseListController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = post_parser

    @jwt_reqired_backoffice('filters', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Filters')
    @swagger.response(response_code=200, summary='Список фильтров', description='-', schema=FilterResponseModelAdmin)
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    # @swagger.parameter(_in='query', name='id',
    #                    description='Список id',
    #                    example=10, required=False, schema={'type': 'array', 'items': {'type': 'string'}})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(paginate_=True, **args)

    @jwt_reqired_backoffice('filters', 'create')
    @swagger.security(JWT=[])
    @swagger.tags('Filters')
    @swagger.response(response_code=201, schema=FilterResponseModelAdmin, summary='Создать новый фильтр')
    @swagger.reqparser(name='FilterCreateModel', parser=post_parser)
    def post(self):
        """Создать новый фильтр"""
        return super().post_()


class FilterController(BaseController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = post_parser

    @jwt_reqired_backoffice('filters', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Filters')
    @swagger.response(response_code=200, summary='Фильтр', description='-', schema=FilterResponseModelAdmin)
    def get(self, filter_id):
        return super().get_(filter_id)

    @jwt_reqired_backoffice('filters', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Filters')
    @swagger.response(response_code=204, summary='Обновить Фильтр', description='-', schema=FilterResponseModelAdmin)
    @swagger.reqparser(name='FilterPutModel', parser=post_parser)
    def put(self, filter_id):
        return super().put_(filter_id)

    @jwt_reqired_backoffice('filters', 'delete')
    @swagger.security(JWT=[])
    @swagger.tags('Filters')
    @swagger.response(response_code=204, summary='Удалить фильтр', description='-', schema=FilterResponseModelAdmin)
    def delete(self, filter_id):
        return super().delete_(filter_id)
