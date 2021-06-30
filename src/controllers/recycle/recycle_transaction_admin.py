from flask_restful import fields, reqparse
from flask_restful_swagger_3 import swagger, Schema

import src.controllers.utils.fields as custom_fields
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.transaction.AdmissionTransaction import AdmissionTransaction
from src.models.utils.enums import STATUS_CHOICES

get_parser = reqparse.RequestParser()
get_parser.add_argument('user', dest='from_', type=str, required=False, location='args')
get_parser.add_argument('admin_pp', dest='admin_pp', type=str, required=False, location='args')
get_parser.add_argument('rec_point', dest='to_', type=str, required=False, location='args')
get_parser.add_argument('status', type=str, choices=STATUS_CHOICES, required=False, location='args')

post_parser = reqparse.RequestParser()
post_parser.add_argument('status', type=str, choices=STATUS_CHOICES, required=True)


class RecycleTransactionItemResponseModel(Schema):
    properties = {
        'filter_id': {'type': 'string', 'description': 'Id фильтра'},
        'filter_name': {'type': 'string', 'description': 'Имя фильтра'},
        'amount': {'type': 'float', 'description': 'Количество сданного ресурса'},
    }


class RecycleTransactionResponseModel(Schema):
    # TODO: актуализировать
    properties = {
        'id': {'type': 'string', 'description': 'Id транзакции'},
        'rec_point_id': {'type': 'string', 'description': 'Id пункта приема'},
        'items': {'type': 'array', 'items': RecycleTransactionItemResponseModel, 'description': 'Сданные ресурсы'},
        'reward': {'type': 'integer', 'description': 'Количество коинов-вознаграждения'},
        'status': {'type': 'string', 'description': 'Статус транзакции'},
        'date': {'type': 'datetime', 'description': 'Дата транзакции'},
        'images': {'type': 'string', 'description': 'Ссылки на изображения'},
    }


resource_fields_ = {
    'id': fields.String,
    'user_id': fields.String(attribute='from_.id'),
    'user_name': fields.String(attribute='from_.name'),
    'admin_pp': fields.String(attribute='admin_pp.id'),
    'admin_pp_name': fields.String(attribute='admin_pp.username'),
    'rec_point_id': fields.String(attribute='to_.id'),
    'items': fields.List(fields.Nested({
        'filter_id': fields.String(attribute='filter.id'),
        'filter_name': fields.String(attribute='filter.name'),
        'amount': fields.Float,
    })),
    'reward': fields.Integer,
    'status': fields.String,
    'date': fields.DateTime('iso8601'),
    'images': fields.List(custom_fields.ImageLink),

}


class RecycleTransactionListController(BaseListController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=RecycleTransactionResponseModel,
                      summary='Список транзакций сдачи отходов',
                      description='-')
    @swagger.parameter(_in='query', name='user', description='Фильтр по пользователю',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='admin_pp', description='Фильтр по админу ПП',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='rec_point', description='Фильтр по ПП',
                       schema={'type': 'string'})
    @swagger.parameter(_in='query', name='status', description='Фильтр по статусам',
                       schema={'type': 'string', 'enum': STATUS_CHOICES})
    def get(self):
        args = get_parser.parse_args()
        args = {k:v for k,v in args.items() if v is not None}
        return super().get_(**args)


class RecycleTransactionController(BaseController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'
    parser = post_parser

    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=RecycleTransactionResponseModel, summary='Транзакция сдачи отхода',
                      description='-')
    def get(self, recycle_id):
        return super().get_(recycle_id)

    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=RecycleTransactionResponseModel, summary='Транзакция сдачи отхода',
                      description='-')
    @swagger.reqparser('RecycleApprove', post_parser)
    def put(self, recycle_id):
        rec_transaction = RecycleTransaction.find_by_id_(recycle_id)
        if rec_transaction is None:
            return {'error': 'RecycleTransaction not fuond'}, 404
        admission_transaction = AdmissionTransaction.objects.filter(action=rec_transaction.id)
        if admission_transaction is None:
            return {'error': 'AdmissionTransaction not fuond'}, 404
        args = post_parser.parse_args()
        rec_transaction.update(set__status=args['status'])
        admission_transaction.update(set__status=args['status'])
        return {'result': 'ok'}, 201