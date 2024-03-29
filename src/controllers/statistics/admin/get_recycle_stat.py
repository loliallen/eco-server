import datetime

from flask_restful import fields, marshal, reqparse, inputs
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseController
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.transaction.AdmissionTransaction import Status
from src.models.user.UserModel import User
from src.utils.roles import jwt_reqired_backoffice


PERIOD = ('day', 'week', 'month', 'year')

get_parser = reqparse.RequestParser()
get_parser.add_argument('user', dest='from_', type=str, required=False, location='args')
get_parser.add_argument('admin_pp', type=str, required=False, location='args')
get_parser.add_argument('date', type=inputs.date, required=False, location='args')
get_parser.add_argument('period', type=str, required=False, choices=PERIOD, location='args')


class RecycleStatDistrictItem(Schema):
    properties = {
        'filter': {'type': 'string', 'description': 'Id фильтра'},
        'name': {'type': 'string', 'description': 'Название фильтра'},
        'total': {'type': 'float', 'description': 'Количество сданного ресурса в кг'},
    }


class RecycleStatisticAdmin(Schema):
    properties = {
        'total': {'type': 'integer', 'description': 'Всего сданных кг'},
        'items': {'type': 'array', 'items': RecycleStatDistrictItem, 'description': 'Сданные ресурсы'},
    }


resource_fields_ = {
    'filter': fields.String,
    'name': fields.String,
    'total': fields.Float
}


class RecycleStatisticController(BaseController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @jwt_reqired_backoffice('dashboard', 'show')
    @swagger.security(JWT=[])
    @swagger.tags('Statistic')
    @swagger.response(response_code=201, schema=RecycleStatisticAdmin, summary='Статистика сдачи отхода',
                      description='-')
    @swagger.parameter(_in='query', name='period', description='Фильтр по периоду',
                       schema={'type': 'string', 'enum': PERIOD})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        period = args.pop('period', None)
        if period:
            today = datetime.datetime.utcnow().date()
            period_dict = {
                'day': today,
                'week': today - datetime.timedelta(days=7),
                'month': today - datetime.timedelta(days=30),
                'year': today - datetime.timedelta(days=365),
            }
            args['date__gte'] = period_dict[period]
        stat = RecycleTransaction.get_statistic(**args)
        stat = list(stat)
        # фильтров у нас не много, общую сумму можно и здесь посчитать
        total = sum(i['total'] for i in stat)
        return {
            'total': total,
            'items': marshal(stat, resource_fields_),
        }
