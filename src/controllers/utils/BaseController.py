import json
from ast import literal_eval

from flask_restful import Resource, marshal
from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError


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
        return marshal(json.loads(obj.to_json()), self.resource_fields)

    def put_(self, id):
        updates = self.parser.parse_args()
        obj = self.model.update_(id, updates)
        if not obj:
            return not_found(self.name, id)

        return marshal(json.loads(obj.to_json()), self.resource_fields)

    def delete_(self, id):
        obj = self.model.delete_(id)
        if not bool(obj):
            return not_found(self.name, id)
        return marshal(json.loads(obj.to_json()), self.resource_fields)


class BaseListController(Resource):
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None

    def get_(self):
        objs = self.model.read_()
        return marshal(json.loads(objs.to_json()), self.resource_fields)

    def post_(self):
        args = self.parser.parse_args()
        try:
            obj = self.model.create_(**args).to_json()
        except DuplicateKeyError as ex:
            return {"message": handle_duplicate_error(ex)}, 400
        except NotUniqueError as ex:
            return {"message": handle_unique_error(ex)}, 400
        return marshal(json.loads(obj), self.resource_fields)
