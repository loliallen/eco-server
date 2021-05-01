from flask_restful import reqparse, fields

from controllers.utils import fields as custom_fields
from controllers.utils.BaseController import BaseListController, BaseController
from models.partner.PartnerModel import Partner

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, location='form')


resource_fields_ = {
    'id': fields.String(attribute=lambda x: x['_id']['$oid']),
    'name': fields.String,
    'points': custom_fields.Dict,
    'products': custom_fields.Dict,
}


class PartnerListController(BaseListController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    parser = post_parser

    def get(self):
        return super().get_()

    def post(self):
        return super().post_()


class PartnerController(BaseController):
    resource_fields = resource_fields_
    model = Partner
    name = 'Partner'
    post_parser = post_parser

    def get(self, partner_id):
        return super().get_(partner_id)

    def put(self, partner_id):
        return super().put_(partner_id)

    def delete(self, partner_id):
        super().delete_(partner_id)
