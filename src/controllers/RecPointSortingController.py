from flask_restful import Resource, request
from bson.objectid import ObjectId
from flask import jsonify
from mongoengine.queryset import QuerySet

import src.models.RecPointModel as RecPoint
import src.models.FilterModel as FilterModel
import src.models.ReceptionTypeModel as ReceptionTypeModel
import src.models.ReceptionTargetModel as ReceptionTargetModel
from src.utils.JsonEncoder import JSONEncoder


class RecPointsSorting(Resource):
    ''' This class sort Recycle Points '''

    def get(self):
        '''
        :arg
            'id':[ObjectId] - list of sought accept_types
            'recep_target': ObjectId - sought reception target
            'recep_type': ObjectId - sought reception types
        :return:
            [
            RecPoints
            ]
        '''
        args = request.json

        res_list = []

        if not ("id" and "recep_type" and "recep_target" in args):
            return {"message": "Not passed query parameter id or recep_type or recep_target"}, 403

        if args['id']:

            rec_points_res = []

            for item in args['id']:
                fl = FilterModel.find_by_id(item)
                if not bool(fl):
                    return {"message": "Filter not found id={}".format(args['id'])}, 404
                else:
                    rec_points_res = RecPoint.filter_by_accept_type(fl)

                    res_list = list(set(res_list + rec_points_res))

            print(len(res_list))

            if not res_list:
                return jsonify(res_list)

        else:
            res_list = list(FilterModel.read())

        recep_target = ReceptionTargetModel.find_by_id(args['recep_target'])

        if not recep_target:
            return {"message": "Reception Target not found id={}".format(args['recep_target'])}, 404

        res_list = RecPoint.filter_by_reception_target(recep_target , res_list)

        if not res_list:
            return jsonify(res_list)

        recep_type = ReceptionTypeModel.find_by_id(args['recep_type'])

        if not recep_type:
            return {"message": "Reception Type not found id={}".format(args['recep_type'])}, 404

        res_list = RecPoint.filter_by_reception_type(recep_type ,res_list)

        return jsonify([i.to_jsony() for i in res_list])
