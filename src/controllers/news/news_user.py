from flask_jwt_extended import (
    jwt_required, verify_jwt_in_request, exceptions as jwt_exceptions
)
from flask_restful import reqparse, fields, inputs
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils import fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.news.NewsModel import News
from src.models.user.UserModel import User
from src.utils.roles import role_need, Roles, ADMINS_GROUP

get_parser = reqparse.RequestParser()
get_parser.add_argument('only_advice', dest='is_advice', type=inputs.boolean, required=False, location='args')
get_parser.add_argument('only_my_news', type=inputs.boolean, required=False, location='args')


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
        'is_advice': {'type': 'boolean', 'description': 'Является ли новость советом'},
        'image': {'type': 'string', 'description': 'Ссылка на изображение'},
        'is_approved': {'type': 'boolean', 'description': 'Подтверждена ли новость админом'},
    }


resource_fields_ = {
    'id': fields.String,
    'title': fields.String,
    'text': fields.String,
    'pub_date': fields.DateTime('iso8601'),
    'is_advice': fields.Boolean,
    'image': custom_fields.ImageLink,
    'is_approved': fields.Boolean,
 }


class NewsListController(BaseListController):
    resource_fields = resource_fields_
    model = News
    name = 'News'
    parser = post_parser
    who_can_add_edit_news = ADMINS_GROUP + [Roles.admin_pp]

    # токен - не обязательный параметр
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=200, schema=NewsResponseModel,
                      summary='Список новостей (Может использоваться без jwt токена)',
                      description='-')
    @swagger.parameter(_in='query', name='only_advice', description='Только советы', schema={'type': 'boolean'})
    @swagger.parameter(_in='query', name='only_my_news', description='Новости только моего авторства (Только для админов ПП)',
                       schema={'type': 'boolean'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        only_my_news = args.pop('only_my_news', False)
        if only_my_news:
            try:
                verify_jwt_in_request()
            except jwt_exceptions.NoAuthorizationError:
                return {'error': 'jwt header was not passed into request'}, 403
            else:
                user = User.get_user_from_request()
                if Roles(user.role) not in self.who_can_add_edit_news:
                    return {'error': 'param only_my_news only for admin_pp'}, 403
                args['author'] = user
        else:
            # если не запрошены только созданные мной новости - отдаем только заапрувленные
            args['is_approved'] = True
        return super().get_(**args)

    @jwt_required()
    @role_need(who_can_add_edit_news)
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Создать новость (Только для админов ПП)',
                      description='-')
    @swagger.reqparser(name='NewsCreateModel', parser=post_parser)
    def post(self):
        admin_pp = User.get_user_from_request()
        return super().post_(author=admin_pp, is_approved=False)


class NewsController(BaseController):
    resource_fields = resource_fields_
    model = News
    name = 'News'

    @swagger.tags('News')
    @swagger.response(response_code=201, schema=NewsResponseModel, summary='Новость',
                      description='-')
    def get(self, news_id):
        # тут пользователь может запросить не заапрувленную
        # новость без токена - не страшно)
        return super().get_(news_id)
