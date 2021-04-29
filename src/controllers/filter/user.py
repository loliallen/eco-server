import json
from ast import literal_eval
from pathlib import Path

import werkzeug
from flask_restful import reqparse, marshal_with, fields


from BaseController import BaseListController, BaseController
from src.models.FilterModel import Filter

# setting path from /eco/server for images
REL_PATH = "/statics/filters"
files_storage = Path('./src'+REL_PATH)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, location='form')
parser.add_argument('var_name', type=str, required=True, location='form')
parser.add_argument('key_words', type=literal_eval, required=True, location='form')
parser.add_argument('bad_words', type=literal_eval, required=True, location='form')
parser.add_argument('coins_by_unit', type=float, location='form')
parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

resource_fields_ = {
    'id': fields.String(attribute=lambda x: x['_id']['$oid']),
    'name': fields.String,
    'var_name': fields.String,
    'key_words': fields.List(fields.String),
    'bad_words': fields.List(fields.String),
    "coins_by_unit": fields.Float
}


class FilterControllerList(BaseListController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = parser

    # custom post
    def get(self):
        return super().get_()


class FilterController(BaseController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = parser


    def get(self, filter_id):
        return super().get_(filter_id)