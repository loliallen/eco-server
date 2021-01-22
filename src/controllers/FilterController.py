from ast import literal_eval
import json
import os
import werkzeug
from pathlib import Path 

from flask import request
from flask_restful import Resource, reqparse
import src.models.FilterModel as FilterModel
from werkzeug.utils import secure_filename


# setting path from /eco/server for images
REL_PATH = "/static/filters"
files_storage = Path('./src'+REL_PATH)

class FilterController(Resource):
    """FilterController [summary]
        Path: */api/filters*
    Arguments:
        Resource {[type]} -- [description]
    """
        
    def get(self):
        """[GET] /api/filters
        return
        '''
            [
                {
                    "name": str,
                    "var_name": str,
                    "image": str,
                    "key_words": Array<str>,
                    "bad_words": Array<str>,
                }
            ]
        '''
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
        parser = reqparse.RequestParser()

        _filter = request.form.to_dict()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
       
        args = parser.parse_args()
        file = args['image']
        relp = ""

        if file:
            filename = secure_filename(file.filename)
            relp=filename
            FILES_PATH = files_storage / filename
            file.save(FILES_PATH.resolve())
            

        if "key_words" in _filter:
            _filter["key_words"] = literal_eval(_filter["key_words"])

        if "bad_words" in _filter:
            _filter["bad_words"] = literal_eval(_filter["bad_words"])

        fl = FilterModel.create(**_filter, image=relp).to_json()
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