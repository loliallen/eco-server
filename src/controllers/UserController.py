from flask_restful import Resource, reqparse, Api
from flask import request, make_response, jsonify, render_template, current_app
import werkzeug.datastructures
import json
from pathlib import Path
from uuid import uuid4
from werkzeug.security import check_password_hash
from flask_mail import Message
from flask_login import login_user, logout_user, current_user
import datetime
import jwt

import src.models.UserModel as User
from send_email import send_email
from src.utils.decorators import token_required, check_confirmed

REL_PATH = "/static/users"
files_storage = Path('./src'+REL_PATH)


class UserController(Resource):
    @token_required
    @check_confirmed
    def get(self):
        args = request.args.to_dict()

        if 'username' in args:
            user = User.find_user_by_username(username=args['username'])

            if not user:
                return {"message": "User not found id={}".format(args['id'])}, 404

            return json.loads(user.to_json())

        else:
            users = User.read()
            return json.loads(users.to_json())

    def post(self):
        data = request.json
        parser = reqparse.RequestParser()

        _filter = request.form.to_dict()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()
        file = args['image']
        data['public_id'] = str(uuid4())
        relp = ""

        if file:
            filename = werkzeug.secure_filename(file.filename)
            relp = filename
            FILES_PATH = files_storage / filename
            file.save(FILES_PATH.resolve())

        user = User.create(data, image=relp)
        login_user(user)

        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, current_app.config['SECRET_KEY'], algorithm="HS256")
        confirm_url = Api.url_for(Api(current_app), resource=UserConfirmController, token=token, _external=True)
        html = render_template('email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        message = Message(subject=subject, html=html, recipients=[user.username])
        send_email(message)

        return json.loads(user.to_json())


    @token_required
    @check_confirmed
    def put(self):
        args = request.args.to_dict()
        updates = request.json

        user = None

        if 'id' in args:
            user = User.update(args['id'], updates)
        else:
            user = User.update(str(current_user.id), updates)

        if not user:
            return {"message": "User not found id={}".format(args['id'])}, 404

        return json.loads(user.to_json())


    @token_required
    @check_confirmed
    def delete(self):
        args = request.args

        user = None

        if 'id' in args:
            user = User.delete(args['id'])
        else:
            user = User.delete(str(current_user.id))

        if not user:
            return {"message": "User not found id={}".format(args['id'])}, 404

        return user.to_json()


class TokenAuthentication(Resource):
    def post(self):
        form = request.form.to_dict()

        if not 'username' or not 'password' in form:
            return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

        user = User.find_user_by_username(form['username'])

        if not user:
            return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

        if check_password_hash(user.password, form['password']):
            encoded_jwt = jwt.encode({"some": "payload"}, current_app.config['SECRET_KEY'], algorithm="HS256")
            print(encoded_jwt)
            token = jwt.encode({'public_id': user.public_id}, current_app.config['SECRET_KEY'], algorithm="HS256")
            login_user(user)
            return jsonify({'token': token})

        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})


class UserConfirmController(Resource):
    def get(self, token):
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
        if not 'username' in data:
            return jsonify({'message': 'Invalid token!'}), 401

        user = User.find_user_by_username(username=data['username'])

        if not user:
            return jsonify({'message': 'Invalid token!'}), 401

        if user.confirmed:
            return jsonify({'message': 'Account already confirmed. Please login.'})

        updates = {
            'confirmed': True,
            'confirmed_on': datetime.datetime.utcnow()
        }

        User.update(str(user.id), updates)
        return jsonify({'message': 'You have confirmed your account. Thanks!'})


class UserLogoutController(Resource):
    def get(self, args):
        logout_user()
        return json.loads(current_user.to_json())
