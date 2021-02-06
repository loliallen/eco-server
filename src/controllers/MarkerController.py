import json
from src.controllers.RecPointController import to_document_type
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
import src.models.MarkerModel as Marker  
import src.models.FilterModel as Filter  
from pathlib import Path

import os
import uuid


REL_PATH = "/static/recpoints"
files_storage = Path('./src'+REL_PATH)

class MarkerController(Resource):
    def get(self):
        
        args = request.args.to_dict()

        if "id" in args:
            # single request
            marker = Marker.find_by_id(args["id"])
            return json.loads(marker.to_json())

        else:
            markers = Marker.read()
            return json.loads(markers.to_json())

    def post(self):
        data = request.form.to_dict()
        image = request.files.get("image")     

        directory = str(uuid.uuid1())
        os.makedirs((files_storage / directory).resolve())
        
        relp = None
        # saving image
        if image != None:
            i = uuid.uuid1()
            filename = secure_filename(image.filename)
            relp = directory + "/" + str(i) + "." + filename.split('.').pop()
            file_path = files_storage / relp
            print(file_path.resolve())
            image.save(file_path.resolve())

        marker = Marker.create(data, relp).to_json()
        return json.loads(marker)

    def put(self):
        updates = request.json
        args = request.args.to_dict()

        marker = Marker.update(args['id'], updates)
        if not marker:
            return {"message": "RecPoint not found id={}".format(args['id'])}, 404

        return json.loads(marker.to_json())
    
    def delete(self):
        # TODO
        pass

class MarkerControllerList(Resource):
    def get(self):
        pipeline = [
            { "$match": {} },
            { "$group": { "_id": "$var_name", "name": {"$push": "$name"} } }
        ]

        filters = list(Filter.Filter.objects.aggregate(*pipeline))
        
        return filters

class MarkerControllerListAll(Resource):
    def get(self):
        pipeline = [
            {
                "$unwind": "$filter_vname"
            },
            {
                "$lookup": {
                    "from": "filters",
                    "localField": "filter_vname",
                    "foreignField": "var_name",
                    "as": "data"
                }
            },
            {
                "$unwind": "$data"
            },
            {
                "$group": {
                    "_id": "$filter_vname",
                    "items": {
                        "$push": {
                            "name": "$data.name",
                            "description": "$description",
                            "image": "$image"
                        }
                    }
                }
            } 
        ]
        # pipeline = [
        #     { "$match": {} },
        #     { "$group": { "_id": "$filter_vname", "items": {"$push":{"description": "$description", "image": "$image"}} } }
        # ]

        markers = list(Marker.Marker.objects.aggregate(*pipeline))
        
        return markers