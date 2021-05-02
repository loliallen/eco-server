import json
import os
import uuid
from ast import literal_eval
from pathlib import Path

from bson import ObjectId
from flask import request
from flask_restful import reqparse, fields, marshal
from werkzeug.utils import secure_filename

from controllers.utils import fields as custom_fields
from controllers.utils.BaseController import BaseListController, BaseController, not_found
from src.models.recpoint.RecPointModel import RecPoint

REL_PATH = "/statics/recpoints"
files_storage = Path('./src' + REL_PATH)


get_parser = reqparse.RequestParser()
get_parser.add_argument('coords', type=literal_eval, required=False, location='args')
get_parser.add_argument('filters', type=lambda x: [ObjectId(i) for i in literal_eval(x)], required=False, location='args')
get_parser.add_argument('payback_type', type=str, required=False, location='args')


post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, location='form')
post_parser.add_argument('address', type=str, required=True, location='form')
post_parser.add_argument('partner', type=ObjectId, required=True, location='form')
post_parser.add_argument('payback_type', type=str, required=True, location='form',
                         choices=('free', 'paid', 'partner'))
post_parser.add_argument('reception_type', type=str, required=True, location='form',
                         choices=('recycle', 'utilisation', 'charity'))
post_parser.add_argument('contacts', type=literal_eval, required=False, location='form')
post_parser.add_argument('work_time', type=literal_eval, required=False, location='form')
post_parser.add_argument('accept_types', type=lambda x: [ObjectId(i) for i in literal_eval(x)], required=False, location='form')
post_parser.add_argument('coords', type=literal_eval, required=False, location='form')
post_parser.add_argument('description', type=list, required=False, location='form')
post_parser.add_argument('getBonus', type=bool, required=False, location='form')


resource_fields_ = {
    'id': fields.String(attribute=lambda x: x['_id']['$oid']),
    'name': fields.String,
    'partner': fields.String(attribute=lambda x: x['partner']['$oid']),
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
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    def get(self):
        args = get_parser.parse_args()
        points = json.loads(RecPoint.read_(**args).to_json())
        return marshal(points, resource_fields_)

    def post(self):
        args = post_parser.parse_args()

        directory = str(uuid.uuid1())
        directory_path = files_storage

        images = request.files.getlist('images')
        os.makedirs((directory_path / directory).resolve())
        relps = []
        # saving images
        for (i, image) in enumerate(images):
            filename = secure_filename(image.filename)
            relp = directory + "/" + str(i) + "." + filename.split('.').pop()
            file_path = directory_path / relp
            print(file_path.resolve())
            image.save(file_path.resolve())
            relps.append(relp)

        rec_point = json.loads(RecPoint.create_(**args).to_json())
        return marshal(rec_point, resource_fields_)


class RecPointController(BaseController):
    resource_fields = resource_fields_
    model = RecPoint
    name = 'RecPoint'
    parser = post_parser

    def get(self, rec_point_id):
        return super().get_(rec_point_id)

    def put(self, rec_point_id):
        return super().put_(rec_point_id)

    def delete(self, rec_point_id):
        super().delete_(rec_point_id)
