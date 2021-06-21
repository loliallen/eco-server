from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, inputs
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.news.NewsModel import News

get_parser = reqparse.RequestParser()
get_parser.add_argument('only_advice', dest='is_advice', type=inputs.boolean, required=False, location='args')


class NewsResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'title': {'type': 'string'},
        'text': {'type': 'string'},
        'pub_date': {'type': 'string'},
        'is_advice': {'type': 'boolean'}
    }


resource_fields_ = {
    'id': fields.String,
    'title': fields.String,
    'text': fields.String,
    'pub_date': fields.DateTime('iso8601'),
    'is_advice': fields.Boolean,
 }


class NewsListController(BaseListController):
    resource_fields = resource_fields_
    model = News
    name = 'News'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=200, schema=NewsResponseModel, summary='Список новостей',
                      description='-')
    @swagger.parameter(_in='query', name='only_advice', description='Только советы', schema={'type': 'boolean'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(**args)


class NewsController(BaseController):
    resource_fields = resource_fields_
    model = News
    name = 'News'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Новость',
                      description='-')
    def get(self, news_id):
        return super().get_(news_id)