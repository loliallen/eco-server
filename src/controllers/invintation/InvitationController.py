from flask_restful import Resource
from flask import request, jsonify

import src.models.InvitationModel as Invitation
import json

class InvitationController(Resource):
    def post(self):
        data = request.json

        iv = Invitation.create(data['user_id'])

        return json.loads(iv.to_json()), 201

