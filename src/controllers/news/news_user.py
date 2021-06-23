from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, inputs
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.news.NewsModel import News
from src.utils.roles import role_need, Roles

get_parser = reqparse.RequestParser()
get_parser.add_argument('only_advice', dest='is_advice', type=inputs.boolean, required=False, location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('text', type=str, required=True)
post_parser.add_argument('is_advice', type=bool, required=True)


class NewsResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'id новости'},
        'title': {'type': 'string', 'description': 'Название'},
        'text': {'type': 'string', 'description': 'Текст'},
        'pub_date': {'type': 'string', 'description': 'Дата публикации'},
        'is_advice': {'type': 'boolean', 'description': 'Является ли новость советом'}
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

    @jwt_required()
    @role_need([Roles.admin_pp])
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Создать новость (Только для админов ПП)',
                      description='-')
    @swagger.reqparser(name='NewsCreateModel', parser=post_parser)
    def post(self):
        return super().post_()


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
