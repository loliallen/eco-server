from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseController
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.transaction.AdmissionTransaction import Status
from src.models.user.UserModel import User


class RecycleStatItem(Schema):
    properties = {
        'filter': {'type': 'string', 'description': 'Id фильтра'},
        'name': {'type': 'string', 'description': 'Название фильтра'},
        'total': {'type': 'float', 'description': 'Количество сданного ресурса в кг'},
    }


class RecycleStatistic(Schema):
    properties = {
        'place': {'type': 'integer', 'description': 'Место в общем зачете'},
        'total': {'type': 'integer', 'description': 'Всего сданных кг'},
        'items': {'type': 'array', 'items': RecycleStatItem, 'description': 'Сданные ресурсы'},
    }


resource_fields_ = {
    'filter': fields.String,
    'name': fields.String,
    'total': fields.Float,
}


class RecycleStatisticController(BaseController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Statistic')
    @swagger.response(response_code=201, schema=RecycleStatistic, summary='Статистика сдачи отхода',
                      description='-')
    def get(self):
        user = User.get_user_from_request()
        stat = RecycleTransaction.get_statistic(from_=user, status=Status.confirmed.value)
        stat = list(stat)
        # фильтров у нас не много, общую сумму можно и здесь посчитать
        total = sum(i['total'] for i in stat)
        return {
            'place': 1,  # TODO подсчитывать место
            'total': total,
            'items': marshal(stat, resource_fields_),
        }
