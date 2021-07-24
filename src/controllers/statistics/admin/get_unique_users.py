import datetime

from flask_restful import fields, marshal, reqparse, inputs
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseController
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.transaction.AdmissionTransaction import Status
from src.models.user.UserModel import User
from src.utils.roles import jwt_reqired_backoffice, Roles

PERIOD = ('day', 'week', 'month', 'year')

get_parser = reqparse.RequestParser()
get_parser.add_argument('role', type=str, choices=Roles.choices(), required=False, location='args')
get_parser.add_argument('date_from', dest='confirmed_on__gte', type=inputs.date, required=True, location='args')
get_parser.add_argument('date_to', dest='confirmed_on__lte', type=inputs.date, required=False, location='args')
get_parser.add_argument('period', type=str, required=True, choices=PERIOD, location='args')


# class RecycleStatDistrictItem(Schema):
#     properties = {
#         'filter': {'type': 'string', 'description': 'Id фильтра'},
#         'name': {'type': 'string', 'description': 'Название фильтра'},
#         'total': {'type': 'float', 'description': 'Количество сданного ресурса в кг'},
#     }
#
#
# class RecycleStatistic(Schema):
#     properties = {
#         'total': {'type': 'integer', 'description': 'Всего сданных кг'},
#         'items': {'type': 'array', 'items': RecycleStatDistrictItem, 'description': 'Сданные ресурсы'},
#     }


resource_fields_ = {
    'date': fields.String(attribute=lambda x: "-".join([str(int(i)) for i in x['_id'].values() if i is not None])),
    'cnt': fields.Integer
}


class UsersStatisticController(BaseController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @jwt_reqired_backoffice()
    @swagger.security(JWT=[])
    @swagger.tags('Statistic')
    @swagger.response(response_code=201, summary='Статистика по пользователям',
                      description='-')
    @swagger.parameter(_in='query', name='period', description='Фильтр по периоду',
                       required=True, schema={'type': 'string', 'enum': PERIOD})
    @swagger.parameter(_in='query', name='date_from', description='Дата с',
                       required=True, schema={'type': 'string'})
    @swagger.parameter(_in='query', name='date_to', description='Дата по',
                       required=False, schema={'type': 'string'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        # date: datetime.date = args.pop('date')
        # args['confirmed_on__gte'] = {
        #     'day': date - datetime.timedelta(days=7),
        #     'week': (date - datetime.timedelta(days=30)).replace(day=1),
        #     'month': (date - datetime.timedelta(days=7)).replace(day=1),
        #     'year': date.replace(day=1, month=1, year=date.year-1),
        # }[args.get('period')]
        stat = User.get_statistic(**args)
        return marshal(list(stat), resource_fields_)
