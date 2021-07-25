from flask_jwt_extended import jwt_required
from flask_restful import reqparse, marshal
from flask_restful_swagger_3 import swagger

from src.controllers.recpoint.user.rec_point_user import resource_fields_
from src.controllers.utils.BaseController import BaseListController
from src.models.recpoint.RecPointComment import RecPointComment
from src.models.recpoint.RecPointModel import RecPoint, RECEPTION_TYPE_CHOICES, PAYBACK_TYPE_CHOICES
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, ActionType
from src.models.user.UserModel import User
from src.models.utils.enums import Status

post_parser = reqparse.RequestParser()
post_parser.add_argument('text', type=str, required=True, help='Текст комментария')
post_parser.add_argument('type', type=str, action='append', required=True, help='Массив тем')


class RecPointCommentController(BaseListController):
    model = RecPointComment
    name = 'RecPointComment'
    parser = post_parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201,
                      summary='Комментарий к пункту приема', description='-')
    @swagger.reqparser(name='RecPointCommentCreateModel', parser=post_parser)
    def post(self, rec_point_id):
        user = User.get_user_from_request()
        args = self.parser.parse_args()
        rec_point = RecPoint.find_by_id_(rec_point_id)
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
        return {'status': 'ok'}
