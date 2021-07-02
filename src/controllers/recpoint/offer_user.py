from flask_jwt_extended import jwt_required
from flask_restful import reqparse, marshal
from flask_restful_swagger_3 import swagger

from src.controllers.recpoint.rec_point_user import RecPointResponseModel
from src.controllers.recpoint.rec_point_user import resource_fields_
from src.controllers.utils.BaseController import BaseListController
from src.models.recpoint.RecPointModel import RecPoint, RECEPTION_TYPE_CHOICES, PAYBACK_TYPE_CHOICES
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, ActionType
from src.models.user.UserModel import User
from src.models.utils.enums import Status

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True)
post_parser.add_argument('address', type=str, required=True)
post_parser.add_argument('partner', type=str, required=True)
post_parser.add_argument('payback_type', type=str, required=True,
                         choices=PAYBACK_TYPE_CHOICES)
post_parser.add_argument('reception_type', type=str, required=True,
                         choices=RECEPTION_TYPE_CHOICES)
post_parser.add_argument('contacts', type=str, action='append', required=False)
post_parser.add_argument('work_time', type=dict, required=True)
post_parser.add_argument('accept_types', type=str, action='append', required=False)
post_parser.add_argument('coords', type=float, action='append', required=False)
post_parser.add_argument('description', type=str, required=False)
post_parser.add_argument('getBonus', type=bool, required=False)
post_parser.add_argument('external_images', type=str, action='append', required=False)


class RecPointOfferController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    # @jwt_required()
    # @swagger.security(JWT=[])
    # @swagger.tags('Filters and Recycle Points')
    # @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Список моих предложений пункта приема',
    #                   description='-')
    # def get(self):
    #     user = User.get_user_from_request()
    #     return super().get_(author=user)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Предложить новый пункт приема',
                      description='-')
    @swagger.reqparser(name='RecPointCreateModel', parser=post_parser)
    def post(self):
        user = User.get_user_from_request()
        args = self.parser.parse_args()
        rec_point, error = self._create_obj(**args, author=user)
        if error:
            return error
        AdmissionTransaction.create_(
            action_type=ActionType.add_pp.value,
            action=rec_point,
            status=Status.idle.value,
            user=user
        )
        return marshal(rec_point, self.resource_fields)


class RecPointOfferUpdateController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel,
                      summary='Предложить изменение пункта приема',
                      description='-')
    @swagger.reqparser(name='RecPointPutModel', parser=post_parser)
    def put(self, rec_point_id):
        args = post_parser.parse_args()
        rec_point = RecPoint.find_by_id_(rec_point_id)
        if rec_point is None:
            return {'error': 'RecPoint not found'}, 404
        if rec_point.approve_status != Status.confirmed.value:
            return {'error': "you can't update not confirmed RecPoint"}, 400
        user = User.get_user_from_request()
        obj, error = self._create_obj(**args, author=user, change_by=rec_point)
        if error:
            return error
        AdmissionTransaction.create_(
            action_type=ActionType.update_pp.value,
            action=obj,
            status=Status.idle.value,
            user=user
        )
        return marshal(obj, self.resource_fields)
