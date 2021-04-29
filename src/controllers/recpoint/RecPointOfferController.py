from flask_restful import Resource, request
from bson.objectid import ObjectId
from flask import jsonify
from mongoengine.queryset import QuerySet

import src.models.RecPointOfferModel as RecPointOffer

from src.utils.JsonEncoder import JSONEncoder
import json

class RecPointOfferController(Resource):
    ''' This class sort Recycle Points '''
    def post(self):
        data = request.json

        offer = RecPointOffer.create(data)

        return json.loads(offer.to_json()), 201