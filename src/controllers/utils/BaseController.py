import json

from flask_restful import Resource, marshal_with, marshal


def _not_found(name, id):
    return {"message": f"{name} not found id={id}"}, 404


class BaseController:
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None

    def get_(self, id):
        obj = self.model.find_by_id_(id)
        if not obj:
            return _not_found(self.name, id)
        return marshal(json.loads(obj.to_json()), self.resource_fields)

    def put_(self, id):
        updates = self.parser.parse_args()
        obj = self.model.update_(id, updates)
        if not obj:
            return _not_found(self.name, id)

        return marshal(json.loads(obj.to_json()), self.resource_fields)

    def delete_(self, id):
        obj = self.model.delete_(id)
        if not bool(obj):
            return _not_found(self.name, id)
        return marshal(json.loads(obj.to_json()), self.resource_fields)


class BaseListController:
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None

    def get_(self):
        objs = self.model.read_()
        return marshal(json.loads(objs.to_json()), self.resource_fields)

    def post_(self):
        args = self.parser.parse_args()
        obj = self.model.create_(**args).to_json()
        return marshal(json.loads(obj.to_json()), self.resource_fields)