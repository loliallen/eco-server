from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful_swagger_3 import swagger

from src.controllers.recpoint.rec_point_user import RecPointResponseModel
from src.controllers.recpoint.rec_point_user import resource_fields_
from src.controllers.utils.BaseController import BaseListController
from src.models.recpoint.RecPointModel import RecPoint, RECEPTION_TYPE_CHOICES, PAYBACK_TYPE_CHOICES
from src.models.user.UserModel import User


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


class RecOfferPointController(BaseListController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Список моих предложений пункта приема',
                      description='-')
    def get(self):
        user = User.get_user_from_request()
        return super().get_(author=user)

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=RecPointResponseModel, summary='Предложить новый пункт приема',
                      description='-')
    @swagger.reqparser(name='RecPointCreateModel', parser=post_parser)
    def post(self):
        user = User.get_user_from_request()
        return super().post_(author=user)
