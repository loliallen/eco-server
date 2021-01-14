import json
from flask import request, jsonify
from flask_restful import Resource, reqparse
import models.RecPointModel as RecPoint
from models.PartnerModel import Partner
import models.FilterModel as FilterModel
from ast import literal_eval 
from pprint import pprint

parser = reqparse.RequestParser()

class RecPointController(Resource):
    """RecPointController [summary]
        Path: */api/rec_points*
    Arguments:
        Resource {[type]} -- [description]
    """

    # def get(self):
    #     """[GET]

    #     Returns:
    #         `[
    #             {
    #                 _id: {
    #                     $oid: string
    #                 },
    #                 name: string,
    #                 var_name: string,
    #                 image: string
    #             },
    #             ...
    #         ]`
    #     """

    def get(self):
        """[GET]
                ...
            ]`
        """

        args = request.args.to_dict()


        if "id" in args:
            rec_point = RecPoint.RecPoint.objects(id=args['id']).first()
            if not rec_point:
                return {"message": "RecPoint not found id={}".format(args['id'])}, 404
            rec_point = rec_point
            print(rec_point.to_mongo())
            return json.loads(rec_point.to_json())
        else:
            rec_points = RecPoint.read().select_related(2)
            # rec_points = json.loads(rec_points)
            print(rec_points.as_pymongo())
            res = []
            for rec in rec_points:
                filters = []
                for f in rec["accept_types"]:
                    pprint(f)
                    fl = FilterModel.find_by_id(f.id).to_json()
                    filters.append(f)

                pprint(filters)
                rec["accept_types"] = filters
                # print(rec)
                res.append(json.loads(rec.to_json()))
            # print(res)
            return json.loads(json.dumps(res))

    def post(self):
        """[POST]
        Returns:
            {
             "_id": {
                    "$oid": "5ff976699b960cc236653033"
            },
            "name": "first recpoint",
            "address": "г. Казань, ул.Большая Красная, 55",
            "partner": {
                    "$oid": "5ff8c19ff6d94774d2309734"
            },
            "coords": {
            "lat": 45.23943939747347,
            "lon": 23.47832873246743
            },
            "accept_types": [
            {
                "$oid": "5ff8b5e658bdaf20f718f2d1"
            },
            {
                "$oid": "5ff8de6ca2443b0828e04115"
            }
            ],
            "work_time": {
            "ПН": {
                "1": "8:00-12:00",
                "2": "13:00-18:00"
            },
            "ВТ": {
            "1": "8:00-12:00",
            "2": "13:00-18:00"
        }
    }
   }
            `
        """
    
        __rec_point = request.form.to_dict()

        if "work_time" in __rec_point:
            _w_t = literal_eval(__rec_point["work_time"])
            print(_w_t, type(_w_t))
            w_t = _w_t
            __rec_point["work_time"] = w_t
        
        if "accept_types" in __rec_point:
            __rec_point["accept_types"] = literal_eval(__rec_point["accept_types"])
        if "coords" in __rec_point:
            __rec_point["coords"] = literal_eval(__rec_point["coords"])
        _rec_point = __rec_point

        print(_rec_point)
        # partner

        # if 'partner_id' in _rec_point:
        #     partner = Partner.objects(id=_rec_point['partner_id']).first()
        #     if not partner:
        #         return {"message": "Filter not found id={}"}, 404
        """
        Странный кусок кода

        accept_types.append(FilterModel.Filter.objects(id='5ff8b5e658bdaf20f718f2d1').first())
        accept_types.append(FilterModel.Filter.objects(id='5ff8de6ca2443b0828e04115').first())
        """
        rec_point = RecPoint.create(_rec_point).to_json()
        return json.loads(rec_point)

    def put(self):
        """[PUT]
        Returns:
            [type] -- [description]
        """

        updates = request.json
        args = request.args.to_dict()

        if not "id" in args:
            return {"message": "Not passed query parameter id"}, 403

        rec_point = RecPoint.update(args['id'],updates)
        if not rec_point:
            return {"message": "RecPoint not found id={}".format(args['id'])}, 404

        return json.loads(rec_point.to_json())

    def delete(self):

        args = request.args.to_dict()

        if "id" not in args:
            return {"message": "Not passed query parameter id"}, 403

        rec_point = RecPoint.delete(args['id'])
        if not bool(rec_point):
            return {"message": "RecPoint not found id={}".format(args['id'])}, 404
        return json.loads(rec_point.to_json())

