from functools import wraps
from flask import request

from src.models.statistic.RequestsStatisticModel import RequestsStatistic
from src.models.user.UserModel import User


def collect_stat(get_parser=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if get_parser is not None:
                args_ = get_parser.parse_args()
                params = {k: v for k, v in args_.items() if v is not None}
            else:
                params = request.args
            user = None
            try:
                user = User.get_user_from_request()
            except:
                pass
            RequestsStatistic(
                request_uri=request.path,
                params=params,
                user=user,
                user_agent=request.headers.get('User-Agent')
            ).save()
            return fn(*args, **kwargs)
        return decorator
    return wrapper
