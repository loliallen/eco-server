from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from flask import request
import werkzeug
from pathlib import Path
import json
import os

import src.models.NewsModel as News

REL_PATH = "/statics/news"
files_storage = Path('./src' + REL_PATH)


class NewsController(Resource):
    def get(self):
        args = request.args
        if 'id' in args:
            news = News.find_by_id(args['id'])
            if not news:
                return {"message": "News not found id={}".format(args['id'])}, 404


            #print(files_storage)
            #tory_path / news.file).resolve())
            #print(Path.cwd())

            return json.loads(news.to_json())
        else:
            news = News.read()
            return json.loads(news.to_json())


    def post(self):
        parser = reqparse.RequestParser()

        _news = request.form.to_dict()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()
        image = args['image']

        relp = ""

        if image:
            filename = secure_filename(image.filename)
            relp = filename
            FILES_PATH = files_storage /filename
            image.save(FILES_PATH.resolve())

        news = News.create(header=_news['header'], text=_news['text'], image=relp).to_json()
        return json.loads(news)

    def put(self):
        updates = request.form.to_dict()
        args = request.args.to_dict()

        if not "id" in args:
            return {"message": "Not passed query parameter id"}, 403

        parser = reqparse.RequestParser()

        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        argum = parser.parse_args()

        image = argum['image']

        if image:
            filename = secure_filename(image.filename)
            FILES_PATH = files_storage / filename
            image.save(FILES_PATH.resolve())
            updates['image'] = filename

        news = News.update(args['id'], updates)
        if not news:
            return {"message": "News not found id={}".format(args['id'])}, 404

        return json.loads(news.to_json())


    def delete(self):
        args = request.args.to_dict()

        if "id" not in args:
            return {"message": "Not passed query parameter id"}, 403

        news = News.delete(args['id'])
        if not bool(news):
            return {"message": "News not found id={}".format(args['id'])}, 404

        return json.loads(news.to_json())