from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseController
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.user.UserModel import User


class RecycleCommonStatistic(Schema):
    properties = {
        'users_count': {'type': 'integer', 'description': 'Кол-во пользователей'},
    }


class RecycleCommonStatisticController(BaseController):
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @swagger.tags('Statistic')
    @swagger.response(response_code=201, schema=RecycleCommonStatistic, summary='Общая статистика',
                      description='-')
    def get(self):
        return {
            'users_count': User.objects.count(),
        }
