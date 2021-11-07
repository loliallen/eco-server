from flask_restful import reqparse, fields, inputs
from flask_restful_swagger_3 import swagger
from bson import ObjectId

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.recpoint.RecPointComment import RecPointComment
import src.controllers.utils.fields as custom_fields
from src.utils.roles import jwt_reqired_backoffice

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')
get_parser.add_argument('id', dest='id__in', type=str, action='append', location='args')
get_parser.add_argument('status', type=str, location='args')
get_parser.add_argument('rec_point', type=ObjectId, location='args')
get_parser.add_argument('date_from', dest='date__gt', type=inputs.date, location='args')
get_parser.add_argument('date_to', dest='date__lt', type=inputs.date, location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('text', type=str, required=True, help='Текст комментария')
post_parser.add_argument('type', type=str, action='append', required=True, help='Массив тем')

resource_fields_ = {
    'id': fields.String,
    'rec_point': fields.String(attribute='rec_point.id'),
    'status': fields.String(attribute='transaction.status'),
    'user': fields.String(attribute='user.id'),
    'text': fields.String(),
    'type': fields.List(fields.String()),
    'date': fields.DateTime('iso8601'),
    'images': fields.List(custom_fields.ImageLink),
}


class RecPointCommentListController(BaseListController):
    resource_fields = resource_fields_
    model = RecPointComment
    name = 'RecPointComment'
    parser = post_parser

    @jwt_reqired_backoffice('rec_point_comment', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Comments')
    @swagger.response(response_code=201,
                      summary='Комментарий к пункту приема', description='-')
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='status',
                       description='Фильтр по статусу',
                       required=False, schema={'type': 'string'})
    @swagger.parameter(_in='query', name='date_from',
                       description='Дата с',
                       required=False, schema={'type': 'string', 'format': 'date'})
    @swagger.parameter(_in='query', name='date_to',
                       description='Дата по',
                       required=False, schema={'type': 'string', 'format': 'date'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(paginate_=True, **args)


class RecPointCommentController(BaseController):
    resource_fields = resource_fields_
    model = RecPointComment
    name = 'RecPointComment'
    parser = post_parser

    @jwt_reqired_backoffice('rec_point_comment', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Comments')
    @swagger.response(response_code=201,
                      summary='Комментарий к пункту приема', description='-')
    def get(self, comment_id):
        return super().get_(comment_id)
