import json
from re import A
from flask import request
from flask_restful import Resource, reqparse
import models.ReceptionTargetModel as ReceptionTargetModel
import models.RecPointModel as RecPointModel

parser = reqparse.RequestParser()


class RecepTargetController(Resource):
    """ReceptionTarget [summary]
        Path: */api/reception_target*
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
    #     filter = FilterModel.find_by_id(id).to_json()
    #     print(filter)
    #     return json.loads(filter)

    def get(self):
        """[GET]

        Returns:
            `[
                {
                    _id: {
                        $oid: string
                    },
                    name: string,
                    var_name: string,
                    image: string
                },
                ...
            ]`
        """

        args = request.args.to_dict()

        if "id" in args:
            recep_target = ReceptionTargetModel.ReceptionTarget.objects(id=args['id']).first()
            if not recep_target:
                return {"message": "ReceptionTarget not found id={}".format(args['id'])}, 404

            return json.loads(recep_target.to_json())
        else:
            recep_targets = ReceptionTargetModel.read()
            return json.loads(recep_targets.to_json())

    def post(self):
        """[POST]

        Returns:
            `
            {
                _id: {
                    $oid: string
                },
                name: string,
                var_name: string,
                image: string,
                key_words: string[]
            }
            `
        """
        args = request.args.to_dict()

        if  "id" and "rec_point_id" in args:
            rec_point = RecPointModel.find_by_id(args['rec_point_id'])

            if not rec_point:
                return {"message": "RecPoint not found id={}".format(args['rec_point_id'])}, 404

            recep_target = ReceptionTargetModel.add_recpoint(str(args['id']), rec_point)
            return json.loads(recep_target.to_json())


        else:
            _recep_target = request.json
            recep_target = ReceptionTargetModel.create(_recep_target['name']).to_json()
            return json.loads(recep_target)

    def put(self):
        """[PUT]

        Arguments:
            id {string} -- Filter id

        Returns:
            [type] -- [description]
        """

        updates = request.json
        args = request.args.to_dict()

        if not "id" in args:
            return {"message": "Not passed query parameter id"}, 403

        recep_target = ReceptionTargetModel.update(args['id'], updates)
        if not recep_target:
            return {"message": "Reception Target not found id={}".format(args['id'])}, 404

        return json.loads(recep_target.to_json())

    def delete(self):

        args = request.args.to_dict()

        if "id" not in args:
            return {"message": "Not passed query parameter id"}, 403

        recep_target = ReceptionTargetModel.delete(args['id'])
        if not bool(recep_target):
            return {"message": "Reception Target not found id={}".format(args['id'])}, 404

        return json.loads(recep_target.to_json())
