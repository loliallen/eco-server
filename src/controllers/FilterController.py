from ast import literal_eval
import json
from re import A
from flask import request
from flask_restful import Resource, reqparse
import src.models.FilterModel as FilterModel


parser = reqparse.RequestParser()

class FilterController(Resource):
    """FilterController [summary]
        Path: */api/filters*
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
            filter = FilterModel.find_by_id(args['id'])
            if not filter:
                return {"message": "Filter not found id={}".format(args['id'])}, 404

            return json.loads(filter.to_json())
        else: 
            filters = FilterModel.read()
            print(filters)
            return json.loads(filters.to_json())
    
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
        _filter = request.form.to_dict()

        if "key_words" in _filter:
            _filter["key_words"] = literal_eval(_filter["key_words"])
        print(_filter)
        fl = FilterModel.create(**_filter).to_json()
        return json.loads(fl)

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
            return { "message": "Not passed query parameter id" }, 403
        
        fl = FilterModel.update(args['id'], updates)
        if not fl:
            return { "message": "Filter not found id={}".format(args['id']) }, 404

        return json.loads(fl.to_json())

    def delete(self):

        args = request.args.to_dict()

        if "id" not in args:
            return { "message": "Not passed query parameter id"}, 403

        fl = FilterModel.delete(args['id'])
        if not bool(fl):
            return { "message": "Filter not found id={}".format(args['id']) }, 404

        return json.loads(fl.to_json())