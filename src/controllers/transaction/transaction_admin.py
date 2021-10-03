from flask_restful import fields, reqparse
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, ACTION_TYPE_CHOICES, STATUS_CHOICES
from src.utils.roles import jwt_reqired_backoffice

get_parser = reqparse.RequestParser()
get_parser.add_argument('user', type=str, required=False, location='args')
get_parser.add_argument('status', type=str, choices=STATUS_CHOICES, required=False, location='args')
get_parser.add_argument('action_type', type=str, choices=ACTION_TYPE_CHOICES, required=False, location='args')
get_parser.add_argument('page', type=int, required=False, location='args')
get_parser.add_argument('size', type=int, required=False, location='args')


class AdmissionTransactionResponseModelAdmin(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id транзакции'},
        'action_type': {'type': 'string', 'description': 'Тип действия', 'choices': ACTION_TYPE_CHOICES},
        'action_id': {'type': 'string', 'description': 'Id действия'},
        'eco_coins': {'type': 'string', 'description': 'Количество экокоинов'},
        'status': {'type': 'string', 'description': 'Статус', 'choices': STATUS_CHOICES},
        'description': {'type': 'string', 'description': 'Пояснение к решению апрува'},
        'date': {'type': 'datetime', 'description': 'Дата транзакции'}
    }


resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='user.id'),
    'user_name': fields.String(attribute='user.name'),
    'action_type': fields.String,
    'action_id': fields.String(attribute='action.id'),
    'eco_coins': fields.Integer,
    'status': fields.String,
    'description': fields.String,
    'date': fields.DateTime('iso8601')
}


class AdmissionTransactionListController(BaseListController):
    resource_fields = resource_fields_
    model = AdmissionTransaction
    name = 'AdmissionTransaction'

    @jwt_reqired_backoffice('transactions', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Transaction')
    @swagger.response(response_code=201, schema=AdmissionTransactionResponseModelAdmin,
                      summary='Список транзакций зачислений',
                      description='-')
    @swagger.parameter(_in='query', name='user', description='Фильтр по пользователю',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='status', description='Фильтр по статусам',
                       schema={'type': 'string', 'enum': STATUS_CHOICES})
    @swagger.parameter(_in='query', name='page',
                       description='Номер страницы',
                       example=1, required=False, schema={'type': 'integer'})
    @swagger.parameter(_in='query', name='size',
                       description='Кол-во элементов на странице',
                       example=10, required=False, schema={'type': 'integer'})
    def get(self):
        args = get_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        return super().get_(paginate_=True, **args)


class AdmissionTransactionTransactionController(BaseController):
    resource_fields = resource_fields_
    model = AdmissionTransaction
    name = 'AdmissionTransaction'

    @jwt_reqired_backoffice('transactions', 'read')
    @swagger.security(JWT=[])
    @swagger.tags('Transaction')
    @swagger.response(response_code=201, schema=AdmissionTransactionResponseModelAdmin, summary='Транзакция зачисления',
                      description='-')
    def get(self, transaction_id):
        return super().get_(transaction_id)
