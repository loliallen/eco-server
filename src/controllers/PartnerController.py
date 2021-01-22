import json
from flask import request
from flask_restful import Resource

import src.models.PartnerModel as PartnerModel

class PartnerController(Resource):
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
            partner_model = PartnerModel.objects(args['id']).first()
            if not partner_model:
                return {"message": "Filter not found id={}".format(args['id'])}, 404

            return json.loads(partner_model.to_json())
        else:
            parners = PartnerModel.read()
            return json.loads(parners.to_json())

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
        _partner = request.json
        pn = PartnerModel.create(_partner['name']).to_json()
        return json.loads(pn)

    def put(self):
        """[PUT]
        Returns:
            [type] -- [description]
        """

        updates = request.json
        args = request.args.to_dict()

        if not "id" in args:
            return {"message": "Not passed query parameter id"}, 403

        pn = PartnerModel.update(args['id'], updates)
        if not pn:
            return {"message": "Filter not found id={}".format(args['id'])}, 404

        return json.loads(pn.to_json())

    def delete(self):

        args = request.args.to_dict()

        if "id" not in args:
            return {"message": "Not passed query parameter id"}, 403

        pn = PartnerModel.delete(args['id'])
        if not bool(pn):
            return {"message": "Filter not found id={}".format(args['id'])}, 404

        return json.loads(pn.to_json())