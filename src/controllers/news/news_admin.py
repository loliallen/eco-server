from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.news.NewsModel import News

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('text', type=str, required=True)
post_parser.add_argument('is_advice', type=bool, required=True)

get_parser = reqparse.RequestParser()
get_parser.add_argument('only_advice', dest='is_advice', type=bool, required=False, location='args')


class NewsResponseModel(Schema):
    properties = {
        'id': {'type': 'string'},
        'title': {'type': 'string'},
        'text': {'type': 'string'},
        'pub_date': {'type': 'string'},
        'is_advice': {'type': 'boolean'},
        'image': {'type': 'string'},
    }


resource_fields_ = {
    'id': fields.String,
    'title': fields.String,
    'text': fields.String,
    'pub_date': fields.DateTime('iso8601'),
    'is_advice': fields.Boolean,
    'image': custom_fields.ImageLink
 }


class NewsListController(BaseListController):
    resource_fields = resource_fields_
    model = News
    name = 'News'
    parser = post_parser

    @swagger.tags('News')
    @swagger.response(response_code=200, schema=NewsResponseModel, summary='Список новостей',
                      description='-')
    @swagger.parameter(_in='query', name='only_advice', description='Только советы', schema={'type': 'boolean'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(**args)

    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Создать новость',
                      description='-')
    @swagger.reqparser(name='NewsCreateModel', parser=post_parser)
    def post(self):
        return super().post_()


class NewsController(BaseController):
    resource_fields = resource_fields_
    model = News
    name = 'News'
    parser = post_parser

    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Новость',
                      description='-')
    def get(self, news_id):
        return super().get_(news_id)

    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Обновить новость',
                      description='-')
    @swagger.reqparser(name='NewsPutModel', parser=post_parser)
    def put(self, news_id):
        return super().put_(news_id)

    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Удалить новость',
                      description='-')
    def delete(self, news_id):
        super().delete_(news_id)
