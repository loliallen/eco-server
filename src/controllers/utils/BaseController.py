from ast import literal_eval

from flask import current_app as app
from flask_babel import lazy_gettext as _
from flask_restful import marshal
from flask_restful_swagger_3 import Resource
from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError

from src.models.user.UserModel import User
from src.controllers.utils.pagination import paginate
from src.exceptions.common import FieldError


def not_found(name, id):
    return {"error": _("%(name)s not found id=%(id)s", name=name, id=id)}, 404


def handle_duplicate_error(ex):
    return {"error": _("Not unique: %(value)s", value=ex.details['keyPattern'])}, 400


def handle_unique_error(ex):
    details = literal_eval((str(ex).split('error: ')[1][:-1]))
    return {"error": _("Not unique: $(value)s", value=details['keyPattern'])}, 400


class BaseController(Resource):
    resource_fields = None
    model = None
    name = 'Resource'
    parser = None
    log_settings = {
        'get': False,
        'put': True,
        'delete': True
    }

    def get_(self, id, **kwargs):
        obj = self.model.find_by_id_(id, **kwargs)
        if not obj:
            return not_found(self.name, id)
        if self.log_settings['get']:
            user = User.get_user_from_request()
            app.logger.info(f'({repr(obj)}) was selected by {repr(user)}')
        return marshal(obj, self.resource_fields), 200

    def put_(self, id, **kwargs):
        updates = self.parser.parse_args()
        err, obj = self.update_obj(id, updates, **kwargs)
        if err:
            return err
        if not obj:
            return not_found(self.name, id)
        if self.log_settings['put']:
            user = User.get_user_from_request()
            app.logger.info(f'({repr(obj)}) was updated by {repr(user)}')
        return marshal(obj, self.resource_fields), 202

    def delete_(self, id, **kwargs):
        obj = self.model.delete_(id, **kwargs)
        if obj is None:
            return not_found(self.name, id)
        if self.log_settings['delete']:
            user = User.get_user_from_request()
            app.logger.info(f'({repr(obj)}) was deleted by {repr(user)}')
        return marshal(obj, self.resource_fields), 204

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
    log_settings = {
        'get': False,
        'post': True
    }

    def get_(self, paginate_=False, page=1, size=10, select_related_depth=1, **kwargs):
        objs = self.model.read_(**kwargs)
        if self.log_settings['get']:
            user = User.get_user_from_request()
            app.logger.info(f'{self.name} was selected by {repr(user)}')
        if paginate_:
            return paginate(objs, page, size, self.resource_fields,
                            select_related_depth=select_related_depth)
        return marshal(list(objs), self.resource_fields), 200

    def post_(self, **kwargs):
        args = self.parser.parse_args()
        obj, error = self._create_obj(**args, **kwargs)
        if error:
            return error
        if self.log_settings['post']:
            user = User.get_user_from_request()
            app.logger.info(f'({repr(obj)}) was created by {repr(user)}')
        return marshal(obj, self.resource_fields), 201

    def _create_obj(self, **kwargs):
        """
        :param kwargs:
        :return: obj, error
        """
        try:
            obj = self.model.create_(**kwargs)
        except DuplicateKeyError as ex:
            return None, handle_duplicate_error(ex)
        except NotUniqueError as ex:
            return None, handle_unique_error(ex)
        return obj, None
