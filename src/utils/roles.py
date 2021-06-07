from enum import Enum
from functools import wraps

from src.models.user.UserModel import User


class Roles(Enum):
    user = 'user'
    admin_pp = 'admin_pp'


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