from flask_restful import fields
from flask_restful.fields import MarshallingException

from src.config import Configuration


class Dict(fields.Raw):

    def format(self, value):
        try:
            return dict(value)
        except ValueError as ve:
            raise MarshallingException(ve)


class ImageLink(fields.String):
    def format(self, value):
        if value:
            if str(value).startswith('http'):
                return str(value)
            return Configuration.STATIC_URL + str(value)
