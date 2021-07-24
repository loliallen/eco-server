import datetime

from flask_restful import fields, marshal, reqparse
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseController
from src.models.recpoint.RecPointModel import DISTRICTS
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.utils.roles import jwt_reqired_backoffice

PERIOD = ('day', 'week', 'month', 'year')

get_parser = reqparse.RequestParser()
get_parser.add_argument('period', type=str, required=False, choices=PERIOD, location='args')
get_parser.add_argument('districts', type=str, action='append', required=False, choices=DISTRICTS, location='args')
get_parser.add_argument('filters', type=str, action='append', required=False, location='args')


class RecycleStatItem(Schema):
    properties = {
        'filter': {'type': 'string', 'description': 'Id фильтра'},
        'name': {'type': 'string', 'description': 'Название фильтра'},
        'total': {'type': 'float', 'description': 'Количество сданного ресурса в кг'},
    }


class RecycleStatDistrict(Schema):
    properties = {
        'district': {'type': 'string', 'description': 'Id фильтра'},
        'total': {'type': 'float', 'description': 'Всего сданных кг'},
        'items': {'type': 'array', 'items': RecycleStatItem, 'description': 'Сданные ресурсы'},
    }


class RecycleDistrictsStatistic(Schema):
    properties = {
        'place': {'type': 'integer', 'description': 'Место в общем зачете'},
        'total': {'type': 'integer', 'description': 'Всего сданных кг'},
        'districts': {'type': 'array', 'items': RecycleStatDistrict, 'description': 'Статистика района'},
    }


resource_fields_ = {
    'district': fields.String,
    'total': fields.Float,
    'items': fields.List(fields.Nested({
        'filter': fields.String,
        'name': fields.String,
        'total': fields.Float
    }))
}


class RecycleStatisticDistrictController(BaseController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Statistic')
    @swagger.response(response_code=201, schema=RecycleDistrictsStatistic, summary='Статистика сдачи отхода по районам',
                      description='-')
    @swagger.parameter(_in='query', name='period', description='Фильтр по периоду',
                       schema={'type': 'string', 'enum': PERIOD})
    @swagger.parameter(_in='query', name='districts', description='Районы',
                       schema={'type': 'string', 'enum': DISTRICTS})
    @swagger.parameter(_in='query', name='filters', description='Фильтры',
                       schema={'type': 'string'})
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
        stat = RecycleTransaction.get_statistic_by_district(**args)
        stat = list(stat)
        # фильтров у нас не много, общую сумму можно и здесь посчитать
        total = sum(i['total'] for i in stat)
        return {
            'total': total,
            'districts': marshal(stat, resource_fields_),
        }
