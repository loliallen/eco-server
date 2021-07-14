from flask_restful import reqparse, fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.news.NewsModel import News
from src.models.user.UserModel import User
from src.utils.roles import jwt_reqired_backoffice

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('text', type=str, required=True)
post_parser.add_argument('is_advice', type=bool, required=False)
post_parser.add_argument('is_approved', type=bool, required=False)

get_parser = reqparse.RequestParser()
get_parser.add_argument('only_advice', dest='is_advice', type=bool, required=False, location='args')
get_parser.add_argument('is_approved', type=bool, required=False, location='args')
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


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
    'image': custom_fields.ImageLink,
    'is_approved': fields.Boolean,
    'author': fields.String(attribute='author.id'),
    'author_name': fields.String(attribute='author.name'),
 }


class NewsListController(BaseListController):
    resource_fields = resource_fields_
    model = News
    name = 'News'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=200, schema=NewsResponseModel, summary='Список новостей',
                      description='-')
    @swagger.parameter(_in='query', name='only_advice', description='Только советы', schema={'type': 'boolean'})
    @swagger.parameter(_in='query', name='is_approved', description='Статус апрува', schema={'type': 'boolean'})
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(paginate_=True, **args)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Создать новость',
                      description='-')
    @swagger.reqparser(name='NewsCreateModel', parser=post_parser)
    def post(self):
        user = User.get_user_from_request()
        return super().post_(author=user)


class NewsController(BaseController):
    resource_fields = resource_fields_
    model = News
    name = 'News'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Новость',
                      description='-')
    def get(self, news_id):
        return super().get_(news_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Обновить новость',
                      description='-')
    @swagger.reqparser(name='NewsPutModel', parser=post_parser)
    def put(self, news_id):
        return super().put_(news_id)

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Удалить новость',
                      description='-')
    def delete(self, news_id):
        super().delete_(news_id)
