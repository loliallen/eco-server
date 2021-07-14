from ast import literal_eval

from flask_restful import marshal
from flask_restful_swagger_3 import Resource
from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError

from src.controllers.utils.pagination import paginate
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

    def get_(self, id, **kwargs):
        obj = self.model.find_by_id_(id, **kwargs)
        if not obj:
            return not_found(self.name, id)
        return marshal(obj, self.resource_fields)

    def put_(self, id, **kwargs):
        updates = self.parser.parse_args()
        err, obj = self.update_obj(id, updates, **kwargs)
        if err:
            return err
        if not obj:
            return not_found(self.name, id)

        return marshal(obj, self.resource_fields)

    def delete_(self, id, **kwargs):
        obj = self.model.delete_(id, **kwargs)
        if not bool(obj):
            return not_found(self.name, id)
        return marshal(obj, self.resource_fields)

    def update_obj(self, id, updates, **kwargs):
        try:
            return None, self.model.update_(id, updates, **kwargs)
        except FieldError as ex:
            return ({'error': {ex.field: ex.info}}, 400), None


class BaseListController(Resource):
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None

    def get_(self, paginate_=False, page=1, size=10, select_related_depth=1, **kwargs):
        objs = self.model.read_(**kwargs)
        if paginate_:
            return paginate(objs, page, size, self.resource_fields,
                            select_related_depth=select_related_depth)
        return marshal(list(objs), self.resource_fields)

    def post_(self, **kwargs):
        args = self.parser.parse_args()
        obj, error = self._create_obj(**args, **kwargs)
        if error:
            return error
        return marshal(obj, self.resource_fields)

    def _create_obj(self, **kwargs):
        try:
            obj = self.model.create_(**kwargs)
        except DuplicateKeyError as ex:
            return None, ({"message": handle_duplicate_error(ex)}, 400)
        except NotUniqueError as ex:
            return None, ({"message": handle_unique_error(ex)}, 400)
        return obj, None
