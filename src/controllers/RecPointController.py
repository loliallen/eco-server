import json
from flask import request, jsonify
from flask_restful import Resource, reqparse
import models.RecPointModel as RecPoint
from models.PartnerModel import Partner
import models.FilterModel as FilterModel
from bson import json_util


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
        Returns:
            `[
                ...
            ]`
        """

        args = request.args.to_dict()

        if "id" in args:
            rec_point = RecPoint.RecPoint.objects(id=args['id']).first()
            if not rec_point:
                return {"message": "RecPoint not found id={}".format(args['id'])}, 404

            return json.loads(rec_point.to_json())
        else:
            rec_points = RecPoint.read()
            #print(json_util.dumps([i.to_json() for i in rec_points]).encode('utf-8'))
            return json.loads(rec_points.to_json())

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
        _rec_point = request.json
        partner = Partner.objects(id=_rec_point['partner_id']).first()
        if not partner:
            return {"message": "Filter not found id={}"}, 404
        accept_types = []
        """
        Странный кусок кода

        accept_types.append(FilterModel.Filter.objects(id='5ff8b5e658bdaf20f718f2d1').first())
        accept_types.append(FilterModel.Filter.objects(id='5ff8de6ca2443b0828e04115').first())
        """
        rec_point = RecPoint.create(_rec_point['name'], _rec_point['address'],
                                    partner, _rec_point['point'], accept_types,
                                    _rec_point['work_time']).to_json()
        return json.loads(rec_point)

    def put(self):
        """[PUT]
        Arguments:
            id {string} -- RecPoint id
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
