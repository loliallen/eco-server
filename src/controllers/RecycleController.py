from flask_restful import Resource
from flask import request, jsonify

import src.models.TransactionModel as Transaction
from src.models.UserModel import User


class RecycleController(Resource):
    # recycle
    def post(self):
        data = request.json
        
        data_to = data['to']
        data_ammout = data['ammount']
        data_from = data['qrcode']

        user = User.objects.get(token=data_from)

        transaction = Transaction.create(user_id=user._id, rec_point_id=data_to, ammount=data_ammout)

        return jsonify(transaction.to_json())




