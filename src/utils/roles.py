from enum import Enum
from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from src.models.user.UserModel import User


class Roles(Enum):
    user = 'user'
    admin_pp = 'admin_pp'
    super_admin = 'super_admin'
    moderator = 'moderator'


ADMINS_GROUP = [Roles.super_admin, Roles.moderator]
BACKOFFICE_ACCESS_ROLES = ADMINS_GROUP


def role_need(role_list):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = User.get_user_from_request()
            if Roles(user.role) not in role_list:
                return {'error': 'permission denied'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def jwt_reqired_backoffice(optional=False, fresh=False, refresh=False, locations=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional, fresh, refresh, locations)
            if not get_jwt().get('backoffice', False):
                return {'error': 'token is not backoffice'}, 405
            return fn(*args, **kwargs)
        return decorator
    return wrapper
