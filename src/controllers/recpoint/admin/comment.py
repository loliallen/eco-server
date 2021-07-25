from flask_jwt_extended import jwt_required
from flask_restful import reqparse, marshal, fields
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.recpoint.RecPointComment import RecPointComment
from src.utils.roles import jwt_reqired_backoffice


# get_parser = reqparse.RequestParser()
# get_parser.add_argument('status', type=str, required=False, help='Статус')

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
}


class RecPointCommentListController(BaseListController):
    resource_fields = resource_fields_
    model = RecPointComment
    name = 'RecPointComment'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Comments')
    @swagger.response(response_code=201,
                      summary='Комментарий к пункту приема', description='-')
    def get(self):
        return super().get_(paginate_=True)


class RecPointCommentController(BaseController):
    resource_fields = resource_fields_
    model = RecPointComment
    name = 'RecPointComment'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Comments')
    @swagger.response(response_code=201,
                      summary='Комментарий к пункту приема', description='-')
    def get(self, comment_id):
        return super().get_(comment_id)
