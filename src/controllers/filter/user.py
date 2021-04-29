import json
from ast import literal_eval
from pathlib import Path

import werkzeug
from flask_restful import reqparse, marshal_with, fields

from controllers.utils.BaseController import BaseListController, BaseController
from src.models.filter.FilterModel import Filter
from flask_restful_swagger_3 import swagger, Resource, Schema

# setting path from /eco/server for images
REL_PATH = "/statics/filters"
files_storage = Path('./src'+REL_PATH)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, location='form')
parser.add_argument('var_name', type=str, required=True, location='form')
parser.add_argument('key_words', type=str, required=True, location='form')
parser.add_argument('bad_words', type=str, required=True, location='form')
parser.add_argument('coins_by_unit', type=float, location='form')
#parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
parser_ = parser

resource_fields_ = {
    'id': fields.String(attribute=lambda x: x['_id']['$oid']),
    'name': fields.String,
    'var_name': fields.String,
    'key_words': fields.List(fields.String),
    'bad_words': fields.List(fields.String),
    "coins_by_unit": fields.Float
}


class FilterSchema(Schema):
    properties = {
        'name': {'type': 'string'},
        'var_name': {'type': 'string'},
        'image': {'type': 'string'},
        "key_words": {'type': 'array', 'items': {'type': 'string'}},
        "bad_words": {'type': 'array', 'items': {'type': 'string'}},
    }


class FilterControllerList(Resource, BaseListController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = parser

    @swagger.tags('Filters')
    @swagger.reorder_with(schema=FilterSchema, response_code=200, as_list=True)
    def get(self):
        """Получить список фильтров (тип отхода)"""
        return super().get_()

    @swagger.tags('Filters')
    @swagger.reorder_with(schema=FilterSchema, response_code=200, example=FilterSchema.properties)
    #@swagger.reqparser(name='FilterCreate', parser=parser_)
    def post(self):
        """Создать фильтр (тип отхода)"""
        return super().post_()


class FilterController(Resource, BaseController):
    resource_fields = resource_fields_
    model = Filter
    name = 'Filter'
    parser = parser

    @swagger.tags('Filters')
    @swagger.response(schema=FilterSchema, response_code=200)
    def get(self, filter_id):
        """Получить фильтр (тип отхода)"""
        return super().get_(filter_id)

    @swagger.tags('Filters')
    @swagger.response(schema=FilterSchema, response_code=200)
    def put(self, filter_id):
        """Обновить фильтр"""
        return super().put_(filter_id)

    @swagger.tags('Filters')
    @swagger.response(schema=FilterSchema, response_code=200)
    def delete(self, filter_id):
        """Удалить фильтр"""
        return super().get_(filter_id)
