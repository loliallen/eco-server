from bson import ObjectId
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseListController
from src.controllers.utils.inputs import Id
from src.models.recpoint.RecPointComment import RecPointComment
from src.models.recpoint.RecPointModel import RecPoint
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, ActionType
from src.models.user.UserModel import User
from src.models.utils.enums import Status
from src.controllers.utils import fields as custom_fields

post_parser = reqparse.RequestParser()
post_parser.add_argument('text', type=str, required=True, help='Текст комментария')
post_parser.add_argument('type', type=str, action='append', required=True, help='Массив тем')
post_parser.add_argument('rec_point', type=Id, required=True, help='Id ПП')


resource_fields_ = {
    'id': fields.String,
    'text': fields.String,
    'type': fields.List(fields.String),
    'status': fields.String(attribute='transaction.status'),
    'date': fields.DateTime('iso8601'),
    'images': fields.List(custom_fields.ImageLink),
}


class RecPointCommentController(BaseListController):
    model = RecPointComment
    name = 'RecPointComment'
    parser = post_parser
    resource_fields = resource_fields_

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201,
                      summary='Мои комментарии к пунктам приема', description='-')
    def get(self):
        user = User.get_user_from_request()
        return super().get_(user=user)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201,
                      summary='Комментарий к пункту приема', description='-')
    @swagger.reqparser(name='RecPointCommentCreateModel', parser=post_parser)
    def post(self):
        user = User.get_user_from_request()
        args = self.parser.parse_args()
        rec_point = RecPoint.find_by_id_(args.pop('rec_point'))
        if not rec_point:
            return {'error': 'RecPoint not found'}
        rec_point_comment, error = self._create_obj(**args, user=user, rec_point=rec_point)
        if error:
            return error
        transaction = AdmissionTransaction.create_(
            action_type=ActionType.update_pp.value,
            action=rec_point_comment,
            status=Status.idle.value,
            user=user
        )
        rec_point_comment.update(set__transaction=transaction)
        return marshal(rec_point_comment, resource_fields_)
