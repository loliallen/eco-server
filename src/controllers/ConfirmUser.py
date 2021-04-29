
from flask import request, jsonify
from flask_restful import Resource, reqparse
import src.models.UserModel as UserModel
import src.models.QuestionModel as QuestionModel


class ConfirmUserController(Resource):

    def get(self):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        token = token.split(' ')[1]

        try:
            user = UserModel.User.objects(token=token).first()
            questions = QuestionModel.read()
            return jsonify(questions)
        except:
            return jsonify({'message': 'Error with db code'})


    def post(self):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        token = token.split(' ')[1]

        data = request.json

        try:
            user = UserModel.User.objects(token=token).first()
        except:
            return jsonify({'message': 'Bad token'})


        try:
            question = QuestionModel.read(id=data['id'])

            if data['answer'] == question.correct_answer:
                user.eco_coins_is_avalible = True
                user.eco_coins += 20 # magic number
                user.save()
                return jsonify({'message': 'Success'})
            return jsonify({'message': 'Fail'}), 403

        except:
            return jsonify({'message': 'Error with db code'})
