import json
from flask import request, jsonify
from flask_restful import Resource

from src.models.statistic.StatisticsModel import Statistic, aggr, users
import json


class StatisticController(Resource):
    def get(self):
        args = request.args
        print(args)
        if "date" in args:
            stat = aggr()
            return json.loads(json.dumps(stat))

        stat = Statistic.objects.all()

        return jsonify([i.to_jsony() for i in stat])


class ModlesStaticController(Resource):
    def get(self):
        models = users()

        return jsonify(models)
