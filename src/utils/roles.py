from enum import Enum
from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request


class Roles(Enum):
    user = 'user'
    admin_pp = 'admin_pp'
    super_admin = 'super_admin'
    moderator = 'moderator'
    partner = 'partner'

    @classmethod
    def choices(cls):
        return tuple(i.value for i in cls)


# GROUPS
ADMINS_GROUP = [Roles.super_admin, Roles.moderator]  # админы, модерирующие весь контент
BACKOFFICE_ACCESS_ROLES = ADMINS_GROUP + [Roles.partner]


def role_need(role_list):
    def wrapper(fn):
        from src.models.user.UserModel import User
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = User.get_user_from_request()
            if Roles(user.role) not in role_list:
                return {'error': 'permission denied'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def jwt_reqired_backoffice(view, action, optional=False, fresh=False, refresh=False, locations=None):
    def wrapper(fn):
        from src.models.user.UserModel import User
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional, fresh, refresh, locations)
            if not get_jwt().get('backoffice', False):
                return {'error': 'token is not backoffice'}, 405

            user = User.get_user_from_request()
            if user is None:
                return {'error': 'user not found'}, 404
            if Roles(user.role) not in BACKOFFICE_ACCESS_RULES[view].get(action, []):
                return {'error': 'permission denied'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


BACKOFFICE_ACCESS_RULES = {
    'dashboard': {
        'show': [Roles.super_admin],
    },
    'lookups': {
        'read': [Roles.super_admin],
    },
    'news': {
        'read': ADMINS_GROUP,
        'create': ADMINS_GROUP,
        'edit': ADMINS_GROUP,
        'delete': [Roles.super_admin],
    },
    'users': {
        'read': ADMINS_GROUP,
        'edit': [Roles.super_admin],
        'delete': [Roles.super_admin],
    },
    'filters': {
        'read': ADMINS_GROUP,
        'create': ADMINS_GROUP,
        'edit': ADMINS_GROUP,
        # 'delete': [Roles.super_admin],
    },
    'partner': {
        'read': ADMINS_GROUP + [Roles.partner],
        'create': ADMINS_GROUP,
        'edit': ADMINS_GROUP + [Roles.partner],
        'delete': [Roles.super_admin],
    },
    'rec_point': {
        'read': ADMINS_GROUP,
        'create': ADMINS_GROUP,
        'approve': ADMINS_GROUP,  # апрув предложения нового пп
        'edit': ADMINS_GROUP,
        # 'delete': [Roles.super_admin],
    },
    'rec_point_comment': {
        'read': ADMINS_GROUP,
        'approve': ADMINS_GROUP,  # апрув предложения изменения пп
    },
    # транзакции зачисления экокоинов
    'transactions': {
        'read': ADMINS_GROUP,
    },
    # транзакции сдачи отходов
    'recycle_transaction': {
        'read': ADMINS_GROUP,
        'approve': ADMINS_GROUP,  # апрув транзакции сдачи отходов
    },
    'product': {
        'read': ADMINS_GROUP + [Roles.partner],
        'create': [Roles.super_admin, Roles.partner] + [Roles.partner],
        'edit': [Roles.super_admin, Roles.partner, Roles.moderator] + [Roles.partner],
        'delete': [Roles.super_admin]
    },
    'product_item': {
        'read': ADMINS_GROUP + [Roles.partner],
        'create': [Roles.super_admin, Roles.partner],
        'edit': [Roles.super_admin, Roles.partner, Roles.moderator],
        'delete': [Roles.super_admin],
    },
    'buy_product': {
        'read': ADMINS_GROUP,
    },
    'test': {
        'read': ADMINS_GROUP,
        'create': ADMINS_GROUP,
        'edit': ADMINS_GROUP,
        'delete': [Roles.super_admin],
    },
    'question': {
        'read': ADMINS_GROUP,
        'create': ADMINS_GROUP,
        'edit': ADMINS_GROUP,
        'delete': [Roles.super_admin],
    },
    'test_attempt': {
        'read': ADMINS_GROUP,
        'delete': [Roles.super_admin],
    }
}


def backoffice_role_checker(view, action):
    return role_need(BACKOFFICE_ACCESS_RULES[view][action])


def get_role_schema(role):
    return {
        view: [action for action, roles in actions.items() if role in roles]
        for view, actions in BACKOFFICE_ACCESS_RULES.items()
    }
