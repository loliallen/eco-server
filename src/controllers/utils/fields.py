from flask_restful import fields
from flask_restful.fields import MarshallingException


class Dict(fields.Raw):

    def format(self, value):
        try:
            return dict(value)
        except ValueError as ve:
            raise MarshallingException(ve)
