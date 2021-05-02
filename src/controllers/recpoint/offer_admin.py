from ast import literal_eval

from flask_restful import reqparse, fields

from controllers.utils import fields as custom_fields
from controllers.utils.BaseController import BaseListController, BaseController
from src.models.recpoint.RecPointOfferModel import RecPointOffer

post_parser = reqparse.RequestParser()
post_parser.add_argument('address', type=str, required=True, location='form')
post_parser.add_argument('partner', type=str, required=True, location='form')
post_parser.add_argument('payback_type', type=str, required=True, location='form',
                         choices=('free', 'paid', 'partner'))
post_parser.add_argument('reception_type', type=str, required=True, location='form',
                         choices=('recycle', 'utilisation', 'charity'))
post_parser.add_argument('contacts', type=literal_eval, required=False, location='form')
post_parser.add_argument('work_time', type=literal_eval, required=False, location='form')
post_parser.add_argument('accept_types', type=literal_eval, required=False, location='form')
post_parser.add_argument('coords', type=literal_eval, required=False, location='form')
post_parser.add_argument('description', type=list, required=False, location='form')
post_parser.add_argument('getBonus', type=bool, required=False, location='form')


resource_fields_ = {
    'id': fields.String(attribute=lambda x: x['_id']['$oid']),
    'partner': fields.String,
    'payback_type': fields.String,
    'reception_type': fields.String,
    'work_time': custom_fields.Dict,
    'contacts': fields.List(fields.String),
    'accept_types': fields.List(fields.String(attribute=lambda x: x['$oid'])),
    'coords': fields.List(fields.Float, attribute=lambda x: x['coords']['coordinates']),
    'description': fields.String,
    'getBonus': fields.Boolean,
}


class RecPointListController(BaseListController):
    resource_fields = resource_fields_
    model = RecPointOffer
    name = 'RecPointOffer'
    post_parser = post_parser

    def get(self):
        return super().get_()


class RecPointController(BaseController):
    resource_fields = resource_fields_
    model = RecPointOffer
    name = 'RecPointOffer'
    post_parser = post_parser

    def get(self, rec_point_id):
        return super().get_(rec_point_id)
