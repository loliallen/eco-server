import json
from re import A
from flask import request
from flask_restful import Resource, reqparse
import src.models.ReceptionTypeModel as ReceptionTypeModel
import src.models.RecPointModel as RecPointModel

parser = reqparse.RequestParser()


class RecepTypeController(Resource):
    """ReceptionType [summary]
        Path: */api/reception_types*
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
            recep_type = ReceptionTypeModel.ReceptionType.objects(id=args['id']).first()
            if not recep_type:
                return {"message": "ReceptionType not found id={}".format(args['id'])}, 404

            return json.loads(recep_type.to_json())
        else:
            recep_types = ReceptionTypeModel.read()
            return json.loads(recep_types.to_json())

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

        if "id" and "rec_point_id" in args:
            rec_point = RecPointModel.find_by_id(args['rec_point_id'])

            if not rec_point:
                return {"message": "RecPoint not found id={}".format(args['rec_point_id'])}, 404

            recep_type = ReceptionTypeModel.add_recpoint(str(args['id']), rec_point)
            return json.loads(recep_type.to_json())
        else:
            _recep_type = request.json
            recep_type = ReceptionTypeModel.create(_recep_type['name']).to_json()
            return json.loads(recep_type)

    def put(self):
        """[PUT]

        Arguments:
            id {string} -- ReceptionType id

        Returns:
            [type] -- [description]
        """

        updates = request.json
        args = request.args.to_dict()

        if not "id" in args:
            return {"message": "Not passed query parameter id"}, 403

        recep_type = ReceptionTypeModel.update(args['id'], updates)
        if not recep_type:
            return {"message": "Reception Type not found id={}".format(args['id'])}, 404

        return json.loads(recep_type.to_json())

    def delete(self):

        args = request.args.to_dict()

        if "id" not in args:
            return {"message": "Not passed query parameter id"}, 403

        recep_type = ReceptionTypeModel.delete(args['id'])
        if not bool(recep_type):
            return {"message": "Reception Type not found id={}".format(args['id'])}, 404

        return json.loads(recep_type.to_json())
