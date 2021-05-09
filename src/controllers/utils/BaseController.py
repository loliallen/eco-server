import os
import uuid
from ast import literal_eval

import werkzeug
from flask import request
from flask_restful import marshal
from flask_restful_swagger_3 import Resource
from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError

from src.exceptions.common import FieldError


def not_found(name, id):
    return {"message": f"{name} not found id={id}"}, 404


def handle_duplicate_error(ex):
    return {"Not unique key": ex.details['keyPattern']}


def handle_unique_error(ex):
    details = literal_eval((str(ex).split('error: ')[1][:-1]))
    return {"Not unique key": details['keyPattern']}


class BaseController(Resource):
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None

    def get_(self, id):
        obj = self.model.find_by_id_(id)
        if not obj:
            return not_found(self.name, id)
        return marshal(obj, self.resource_fields)

    def put_(self, id):
        updates = self.parser.parse_args()
        err, obj = self.update_obj(id, updates)
        if err:
            return err
        if not obj:
            return not_found(self.name, id)

        return marshal(obj, self.resource_fields)

    def delete_(self, id):
        obj = self.model.delete_(id)
        if not bool(obj):
            return not_found(self.name, id)
        return marshal(obj, self.resource_fields)

    def update_obj(self, id, updates):
        try:
            return None, self.model.update_(id, updates)
        except FieldError as ex:
            return ({'error': {ex.field: ex.info}}, 400), None


class BaseListController(Resource):
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None
    img_field = None
    img_field_type = str
    img_path = None

    def get_(self):
        objs = self.model.read_()
        return marshal(list(objs), self.resource_fields)

    def post_(self):
        obj, error = self._create_obj()
        if error:
            return error
        return marshal(obj, self.resource_fields)

    def _create_obj(self):
        args = self.parser.parse_args()
        if self.img_field and self.img_path:
            if self.img_field_type is str:
                self.save_img(args)
            if self.img_field_type is list:
                self.save_imgs(args)
        try:
            obj = self.model.create_(**args)
        except DuplicateKeyError as ex:
            return None, ({"message": handle_duplicate_error(ex)}, 400)
        except NotUniqueError as ex:
            return None, ({"message": handle_unique_error(ex)}, 400)
        return obj, None

    def save_img(self, args):
        file = args.get('image')
        if file:
            filename = werkzeug.utils.secure_filename(file.filename)
            path = self.img_path / filename
            file.save(path.resolve())
            args[self.img_field] = filename

    def save_imgs(self, args):
        directory = str(uuid.uuid1())
        directory_path = self.img_path
        images = request.files.getlist('images')
        os.makedirs((directory_path / directory).resolve())
        imgs = []
        # saving images
        for (i, image) in enumerate(images):
            filename = werkzeug.utils.secure_filename(image.filename)
            relp = directory + "/" + str(i) + "." + filename.split('.').pop()
            file_path = directory_path / relp
            image.save(file_path.resolve())
            imgs.append(relp)
        if len(imgs) > 0:
            args[self.img_field] = imgs
