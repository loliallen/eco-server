from flask_jwt_extended import jwt_required
from flask_restful import fields
from flask_restful_swagger_3 import swagger, Schema

from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, ACTION_TYPE_CHOICES, STATUS_CHOICES
from src.models.user.UserModel import User


class AdmissionTransactionResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id транзакции'},
        'action_type': {'type': 'string', 'description': 'Тип действия', 'choices': ACTION_TYPE_CHOICES},
        'action_id': {'type': 'string', 'description': 'Id действия'},
        'eco_coins': {'type': 'string', 'description': 'Количество экокоинов'},
        'status': {'type': 'string', 'description': 'Статус', 'choices': STATUS_CHOICES},
        'date': {'type': 'datetime', 'description': 'Дата транзакции'}
    }


resource_fields_ = {
    'id': fields.String,
    # 'user_id': fields.String(attribute='from_.id'),
    'action_type': fields.String,
    'action_id': fields.String(attribute='action.id'),
    'eco_coins': fields.Integer,
    'status': fields.String,
    'date': fields.DateTime('iso8601')
}


class AdmissionTransactionListController(BaseListController):
    resource_fields = resource_fields_
    model = AdmissionTransaction
    name = 'AdmissionTransaction'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Transaction')
    @swagger.response(response_code=201, schema=AdmissionTransactionResponseModel,
                      summary='Список транзакций зачислений',
                      description='-')
    def get(self):
        return super().get_(user=User.get_user_from_request())


class AdmissionTransactionTransactionController(BaseController):
    resource_fields = resource_fields_
    model = AdmissionTransaction
    name = 'AdmissionTransaction'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Transaction')
    @swagger.response(response_code=201, schema=AdmissionTransactionResponseModel, summary='Транзакция зачисления',
                      description='-')
    def get(self, transaction_id):
        return super().get_(transaction_id, user=User.get_user_from_request())
