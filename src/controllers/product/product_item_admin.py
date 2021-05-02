import json

from flask_restful import reqparse, fields, marshal

from controllers.utils.BaseController import BaseListController, BaseController, not_found
from models.product.ProductItemModel import ProductItem

parser = reqparse.RequestParser()
parser.add_argument('product', type=str, required=True, location='form')
parser.add_argument('contents', type=str, required=True, location='form')

resource_fields_ = {
    'id': fields.String(attribute=lambda x: x['_id']['$oid']),
    'product': fields.String(attribute=lambda x: x['product']['$oid']),
    'contents': fields.String,
    'is_bought': fields.Boolean(attribute=lambda x: bool(x.get('user')))
}


class ProductItemListController(BaseListController):
    resource_fields = resource_fields_
    model = ProductItem
    name = 'ProductItem'
    parser = parser

    def get(self):
        return super().get_()

    def post(self):
        return super().post_()


class ProductItemController(BaseController):
    resource_fields = resource_fields_
    model = ProductItem
    name = 'ProductItem'
    parser = parser

    def get(self, product_id):
        return super().get_(product_id)

    def put(self, product_id):
        updates = self.parser.parse_args()
        obj = self.model.update_(product_id, updates)
        if not obj:
            return not_found(self.name, product_id)
        if obj.user is not None:
            return {'error': 'can\' put, because product already bought'}, 400
        return marshal(json.loads(obj.to_json()), self.resource_fields)
