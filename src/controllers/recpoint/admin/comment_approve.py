import json

from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.config import Configuration
from src.controllers.utils.BaseController import BaseListController
from src.models.recpoint.RecPointComment import RecPointComment
from src.models.recpoint.RecPointModel import RecPoint
from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.utils.enums import Status, STATUS_CHOICES
from src.utils.roles import jwt_reqired_backoffice

post_parser = reqparse.RequestParser()
post_parser.add_argument('approve_status', type=str, choices=(Status.confirmed.value,
                                                              Status.dismissed.value), required=True)
post_parser.add_argument('eco_coins', type=int,  required=False)
post_parser.add_argument('description', type=str,  required=False)


class CommentsApproveController(BaseListController):
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Comments')
    @swagger.response(response_code=201,
                      summary='Апрув комментария об изменении ПП',
                      description='-')
    @swagger.reqparser(name='CommentApproveModel', parser=post_parser)
    def post(self, comment_id):
        args = post_parser.parse_args()
        status = args['approve_status']
        comment = RecPointComment.find_by_id_(comment_id)
        if comment is None:
            return {'error': 'Comment not found'}, 404

        if comment.transaction.status != Status.idle.value:
            return {'error': 'Transaction status not idle'}, 404


        if status == Status.dismissed.value:
            to_add = 0
        else:
            to_add = args['eco_coins'] or Configuration.ECO_COINS_BY_OFFER_NEW_REC_POINT

        comment.transaction.update(
            set__eco_coins=to_add,
            set__status=status,
            set__description=args['description'],
        )
        if to_add > 0:
            comment.user.add_freeze_coins(to_add)
        return {'status': 'ok'}
