import json

from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.config import Configuration
from src.controllers.recpoint.admin.rec_point_admin import RecPointResponseModelAdmin, resource_fields_
from src.controllers.utils.BaseController import BaseListController
from src.models.recpoint.RecPointModel import RecPoint
from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.utils.enums import Status, STATUS_CHOICES
from src.utils.roles import jwt_reqired_backoffice

post_parser = reqparse.RequestParser()
post_parser.add_argument('approve_status', type=str, choices=(Status.confirmed.value,
                                                              Status.dismissed.value), required=True)
post_parser.add_argument('eco_coins', type=int,  required=False)
post_parser.add_argument('description', type=str,  required=False)


class RecPointOfferApproveController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    @jwt_reqired_backoffice('rec_point', 'approve')
    @swagger.security(JWT=[])
    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModelAdmin,
                      summary='Апрув добавления нового ПП',
                      description='-')
    @swagger.reqparser(name='RecPointApproveModel', parser=post_parser)
    def post(self, rec_point_id):
        args = post_parser.parse_args()
        status = args['approve_status']
        rec_point = RecPoint.find_by_id_(rec_point_id)
        if rec_point is None:
            return {'error': 'RecPoint not found'}, 404
        if rec_point.approve_status != Status.idle.value:
            return {'error': 'RecPoint status not idle'}, 404
        admission_transaction = AdmissionTransaction.objects.filter(
            user=rec_point.author,
            action=rec_point).first()
        if admission_transaction is None:
            return {'error': 'AdmissionTransaction not found'}, 404
        action = rec_point

        if status == Status.dismissed.value:
            rec_point.delete()
            action = None
            to_add = 0
        else:
            rec_point.update(set__approve_status=status)
            to_add = args['eco_coins'] or Configuration.ECO_COINS_BY_OFFER_NEW_REC_POINT

        admission_transaction.update(
            set__eco_coins=to_add,
            set__status=status,
            set__description=args['description'],
            set__action=action,
        )
        if to_add > 0:
            rec_point.author.add_freeze_coins(to_add)
        return {'status': 'ok'}
