from flask_restful import Resource
import json
import src.models.QuestionModel as QuestionModel


class QuestionList(Resource):
    def get(self):

        questions = QuestionModel.read()

        return json.loads(questions.to_json())
        
    def post(self):
        data = request.form.to_dict()  


        question = QuestionModel.create(data).to_json()
        return json.loads(question)