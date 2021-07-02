import json

from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.config import Configuration
from src.controllers.recpoint.rec_point_admin import RecPointResponseModel, resource_fields_
from src.controllers.utils.BaseController import BaseListController
from src.models.recpoint.RecPointModel import RecPoint
from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.utils.enums import Status, STATUS_CHOICES

post_parser = reqparse.RequestParser()
post_parser.add_argument('approve_status', type=str, choices=STATUS_CHOICES, required=True)
post_parser.add_argument('eco_coins', type=int,  required=False)
post_parser.add_argument('description', type=str,  required=False)


class RecPointOfferApproveController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Апрув изменения/добавления ПП приема',
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

        if status == Status.idle.value:
            admission_transaction.update(set__description=args['description'])
            return {'status': 'ok'}

        action_after_save = rec_point.change_by or rec_point

        if status == Status.dismissed.value:
            rec_point.delete()
            if rec_point.change_by is None:
                action_after_save = None
            to_add = 0
        else:
            if rec_point.change_by is None:
                # если это добавление нового ПП
                rec_point.update(set__approve_status=status)
                to_add = args['eco_coins'] or Configuration.ECO_COINS_BY_OFFER_NEW_REC_POINT
            else:
                # иначе редактирование информации о старом ПП
                # копируем новую инфу из апдейта в старый ПП
                d = json.loads(rec_point.to_json())
                d.pop('_id')
                RecPoint.update_(rec_point.change_by.id, d)
                rec_point.delete()  # удаляем апдейт
                to_add = args['eco_coins'] or Configuration.ECO_COINS_BY_OFFER_CHANGE_REC_POINT
        admission_transaction.update(
            set__eco_coins=to_add,
            set__status=status,
            set__description=args['description'],
            set__action=action_after_save,
        )
        rec_point.author.add_freeze_coins(to_add)
        return {'status': 'ok'}
