from flask_restful import Resource

import src.models.TransactionModel as TransactionModel

class TransactionController(Resource):
    def get(self):
        transactions = TransactionModel.read()

        return jsonify([i.to_jsony() for i in transactions])


