from cerberus import Validator
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, marshal
from flask_restful_swagger_3 import swagger, Schema

from src.config import Configuration
from src.controllers.utils.BaseController import BaseListController, BaseController
from src.models.filter.FilterModel import Filter
from src.models.recycle.RecycleTransaction import RecycleTransaction, RecycleTransactionItem
from src.models.transaction.AdmissionTransaction import AdmissionTransaction, Status
from src.models.user.UserModel import User
from src.utils.roles import role_need, Roles


def validate_item(value):
    SCHEMA = {
        'filter_type': {'type': 'string', 'required': True},
        'amount': {'type': 'float', 'required': True},
    }
    v = Validator(SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(v.errors)

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_token', type=str, required=True, help='qr код пользователя')
post_parser.add_argument('items', type=validate_item, required=True, action='append')

old_post_parser = reqparse.RequestParser()
old_post_parser.add_argument('user_token', type=str, required=True, help='qr код пользователя')
old_post_parser.add_argument('filter_type', type=str, required=True, help='тип сдаваемого отхода (фильтра)')
old_post_parser.add_argument('amount', type=int, required=True, help='количество отхода')


class RecycleTransactionItemCreateModel(Schema):
    properties = {
        'filter_type': {'type': 'string', 'description': 'Id фильтра'},
        'amount': {'type': 'float', 'description': 'Количество сданного ресурса в кг'},
    }


class RecycleTransactionCreateModel(Schema):
    properties = {
        'user_token': {'type': 'string', 'description': 'qr код пользователя'},
        'items': {'type': 'array',
                  'items': RecycleTransactionItemCreateModel,
                  'description': 'Список сдаваемых материалов'},
    }


class RecycleTransactionResponseModel(Schema):
    properties = {
        'id': {'type': 'string', 'description': 'Id транзакции'},
        'rec_point_id': {'type': 'string', 'description': 'Id пункта приема'},
        'filter_id': {'type': 'string', 'description': 'Id фильтра'},
        'filter_name': {'type': 'string', 'description': 'Имя фильтра'},
        'amount': {'type': 'float', 'description': 'Количество сданного ресурса'},
        'reward': {'type': 'integer', 'description': 'Количество коинов-вознаграждения'},
        'status': {'type': 'string', 'description': 'Статус транзакции'},
        'date': {'type': 'datetime', 'description': 'Дата транзакции'}
    }


resource_fields_ = {
    'id': fields.String,
    'rec_point_id': fields.String(attribute='to_.id'),
    'filter_id': fields.String(attribute='filter_type.id'),  # old
    'filter_name': fields.String(attribute='filter_type.name'),  # old
    'amount': fields.Float,  # old
    'items': fields.List(fields.Nested({
        'filter_id': fields.String(attribute='filter.id'),
        'filter_name': fields.String(attribute='filter.name'),
        'amount': fields.Float,
    })),
    'reward': fields.Integer,
    'status': fields.String,
    'date': fields.DateTime('iso8601')
}


class RecycleTransactionListController(BaseListController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'
    parser = post_parser

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=RecycleTransactionResponseModel,
                      summary='Список транзакций сдачи отходов',
                      description='-')
    def get(self):
        return super().get_(from_=User.get_user_from_request())

    @jwt_required()
    @role_need([Roles.admin_pp])
    @swagger.security(JWT=[])
    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=RecycleTransactionResponseModel,
                      summary='Зафиксировать сдачу отхода (Только для админов пункта  приема)',
                      description='-')
    @swagger.expected(RecycleTransactionCreateModel, required=True)
    def post(self):
        if request.json and request.json.get('items') is None:
            args = old_post_parser.parse_args()
            return self.old_post(args)
        args = self.parser.parse_args()
        pp_admin = User.get_user_from_request()
        user = User.objects.filter(token=args.pop('user_token')).first()
        if not user:
            return {'error': 'user by token not found'}, 400

        items = {i['filter_type']: i['amount'] for i in args['items']}
        filters_ids = list(items.keys())
        if len(set(filters_ids)) < len(args['items']):
            return {'error': 'some filters are duplicated'}, 400
        filters = Filter.objects.filter(id__in=filters_ids).all()
        not_found_filters_ids = set(filters_ids) - {str(i.id) for i in filters}
        if len(not_found_filters_ids) > 0:
            return {'error': f'filters not found: {not_found_filters_ids}'}, 400
        items = [RecycleTransactionItem(filter=filter_, amount=items[str(filter_.id)]) for filter_ in filters]
        reward = sum(i.filter.coins_per_unit * i.amount for i in items)

        # если больше 10 кг, то оставляем на проверку (статус idle), иначе confirmed
        need_approve = any(i.amount > Configuration.WEIGHT_RECYCLE_TO_NEED_APPROVE for i in items)
        status = Status.idle if need_approve else Status.confirmed
        # создаем транзакцию на сдачу отходов
        rec_transaction, error = self._create_obj(
            from_=user,
            to_=pp_admin.attached_rec_point,
            admin_pp=pp_admin,
            items=items,
            reward=reward,
            status=status.value
        )
        if error:
            return error
        # создаем транзакцию на зачисление экокоинов
        AdmissionTransaction.create_(
            action_type='r',  # recycle
            action=rec_transaction,
            status=status.value,
            user=user.id,
            eco_coins=rec_transaction.reward
        )
        # если статус подтверждена - то сразу зачисляем замороженные экокоины
        if status == Status.confirmed:
            user.add_freeze_coins(rec_transaction.reward)
        return marshal(rec_transaction, self.resource_fields)

    def old_post(self, args):
        pp_admin = User.get_user_from_request()
        args['to_'] = pp_admin.attached_rec_point
        user = User.objects.filter(token=args.pop('user_token')).first()
        if not user:
            return {'error': 'user by token not found'}, 400
        filter = Filter.find_by_id_(_id=args['filter_type'])
        if not user:
            return {'error': 'user by token not found'}, 400
        args['from_'] = user.id
        # если больше 10 кг, то оставляем на проверку (статус idle), иначе confirmed
        status = Status.idle if args['amount'] > Configuration.WEIGHT_RECYCLE_TO_NEED_APPROVE else Status.confirmed
        # создаем транзакцию на сдачу отходов
        rec_transaction, error = self._create_obj(
            **args,
            admin_pp=pp_admin,
            reward=filter.coins_per_unit * args['amount'],
            status=status.value
        )
        if error:
            return error
        # создаем транзакцию на зачисление экокоинов
        AdmissionTransaction.create_(
            action_type='r',  # recycle
            action=rec_transaction,
            status=status.value,
            user=user.id,
            eco_coins=rec_transaction.reward
        )
        # если статус подтверждена - то сразу зачисляем замороженные экокоины
        if status == Status.confirmed:
            user.add_freeze_coins(rec_transaction.reward)
        return marshal(rec_transaction, self.resource_fields)


class RecycleTransactionController(BaseController):
    resource_fields = resource_fields_
    model = RecycleTransaction
    name = 'RecycleTransaction'

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=RecycleTransactionResponseModel, summary='Транзакция сдачи отхода',
                      description='-')
    def get(self, recycle_id):
        return super().get_(recycle_id, from_=User.get_user_from_request())
