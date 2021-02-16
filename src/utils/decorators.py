from flask_login import current_user
from flask import request, jsonify, current_app
from functools import wraps
import jwt

from src.models import UserModel


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(token)

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        token = token.split(' ')[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            user = UserModel.User.objects(public_id=data['public_id']).first()

        except:
            return jsonify({'message': 'token is invalid'})

        return f(user, *args, **kwargs)

    return decorator


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return jsonify({'warning': 'Please confirm your account!'})
        return func(*args, **kwargs)

    return decorated_function