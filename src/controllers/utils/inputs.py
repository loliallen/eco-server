from bson import ObjectId
from flask_babel import lazy_gettext as _
from marshmallow import fields, validate


class Email(fields.Email):
    swagger_type = 'string'

    def __call__(self, *args, **kwargs):
        return self._validate(*args, **kwargs)

    def _validate(self, value):
        super()._validate(value)
        return value


class Password(fields.String):
    swagger_type = 'string'
    help_msg = _('minimum 8 sign, minimum 1 digit and 1 letter')

    def __init__(self, *args, **kwargs):
        super().__init__(validate=validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d_!@#$%^&*]{8,}$'),
                         *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._validate(*args, **kwargs)

    def _validate(self, value):
        super()._validate(value)
        return value


class NotEmptyString(fields.String):
    swagger_type = 'string'
    help_msg = 'не пустое'

    def __init__(self, *args, **kwargs):
        super().__init__(validate=validate.Length(min=1),
                         *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._validate(*args, **kwargs)

    def _validate(self, value):
        super()._validate(value)
        return value


class Id(ObjectId):
    swagger_type = 'string'
    help_msg = 'Id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
