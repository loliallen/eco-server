from functools import wraps

import werkzeug
from flask_babel import LazyString, force_locale
from flask_restful import reqparse
from flask.json import JSONEncoder as BaseEncoder
from flask_restful_swagger_3 import Api, Schema, DefinitionEncoder


class JSONEncoder(BaseEncoder):
    def default(self, o):
        if isinstance(o, LazyString):
            return str(o)
        return super().default(o)


def default(self, obj):
    if isinstance(obj, LazyString):
        with force_locale('ru_RU'):
            return str(obj)
    return obj.definitions()


DefinitionEncoder.default = default


class CustomApi(Api):

    def _Api__build_request_body(self, request_body):
        req_schema, req_body = super(CustomApi, self)._Api__build_request_body(request_body)
        if request_body.get('content'):
            req_body['requestBody']['content'] = request_body['content']
        if request_body.get('additional_schema'):
            model = self._Api__build_model(request_body.get('additional_schema'))
            if req_schema:
                req_schema.update(model["reusable_schema"])
            else:
                req_schema = model["reusable_schema"]
        return req_schema, req_body


class FileSchema(Schema):
    properties = {
        'file': {
            'type': 'string',
            'format': 'binary',
        }
    }
    type = 'object'


class FilesArraySchema(Schema):
    properties = {
        'files': {
            'type': 'array',
            'items': {
                'type': 'string',
                'format': 'binary',
            }
        }
    }
    type = 'object'


def mark_files_request(is_list=False):
    def decorated(func):
        schema = FileSchema
        if is_list:
            schema = FilesArraySchema
        func.__request_body = {
            "schema": {},
            "required": True,
            "content": {
                'multipart/form-data': {
                    'schema': schema.reference()
                }
            },
            "additional_schema": schema
        }

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return wrapper

    return decorated


post_parser_with_files = reqparse.RequestParser()
post_parser_with_files.add_argument('files', type=werkzeug.datastructures.FileStorage,
                                    required=False, action='append', location='files')

post_parser_with_file = reqparse.RequestParser()
post_parser_with_file.add_argument('file', type=werkzeug.datastructures.FileStorage,
                                    required=False, action='append', location='files')


class OkSchema(Schema):
    properties = {
        'status': { 'type': 'string' }
    }
