from flask_restful import Resource, reqparse
from flask import request, jsonify

import src.models.TransactionModel as Transaction
from src.models.UserModel import User
from src.utils.dict import get as get_field

from pathlib import Path

import werkzeug
from werkzeug.utils import secure_filename


REL_PATH = "/statics/transactions"
files_storage = Path('./src'+REL_PATH)

class RecycleController(Resource):
    def get(self):
        args = request.args.to_dict()

        instance_id = get_field('id', args)
        instance_type = get_field('type', args)

        transactions = Transaction.read(instance_id, instance_type)

        return jsonify([i.to_jsony() for i in transactions])

    # recycle
    def post(self):
        parser = reqparse.RequestParser()


        data = request.form.to_dict()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        
        
        args = parser.parse_args()
        file = args['image']
        relp = ""

        if file:
            filename = secure_filename(file.filename)
            relp=filename
            FILES_PATH = files_storage / filename
            file.save(FILES_PATH.resolve())

        data_to = data['to']
        data_ammout = data['ammount']
        data_from = data['qrcode']
        data_filter = data['filter_type']

        user = User.objects(token=data_from).first()
        
        transaction = Transaction.create(user_id=user.id, rec_point_id=data_to, ammount=data_ammout, filter=data_filter, image=relp)

        return jsonify(transaction.to_jsony())




