from src.models.StatisticsModel import Statistic
from src.models.UserModel import User
from flask import Request

class Collector(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        stat = Statistic()
        print("env", environ)
        request = Request(environ)
        stat.request_uri = environ['RAW_URI']
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            user = User.objects(id=data['_id']).first()
            stat.user = user._id
        stat.save()
        return self.app(environ, start_response)
