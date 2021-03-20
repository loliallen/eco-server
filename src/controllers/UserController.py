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

from mongoengine.errors import NotUniqueError

import src.models.UserModel as User
import src.models.InvitationModel as Invitation
from src.utils.send_email import send_email
from src.utils.decorators import token_required, check_confirmed
from src.utils.dict import get as get_field
from src.utils.generator import generate_code

REL_PATH = "/statics/users"
files_storage = Path('./src'+REL_PATH)


class UserController(Resource):
    # @token_required
# @check_confirmed
    def get(self):
        args = request.args.to_dict()
        print(current_app)

        if 'username' in args:
            user = User.find_user_by_username(username=args['username'])

            if not user:
                return {"message": "User not found id={}".format(args['id'])}, 404

            return json.loads(user.to_json())

        else:
            users = User.read()
            return json.loads(users.to_json())

    def post(self):
        data = request.form.to_dict()
        argv = request.args.to_dict()

        parser = reqparse.RequestParser()

        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()
        file = args['image']
        relp = ""

        if file:
            filename = werkzeug.secure_filename(file.filename)
            relp = filename
            FILES_PATH = files_storage / filename
            file.save(FILES_PATH.resolve())
        try:
            user = User.create(data, image=relp)
            if "code" in argv:
                print("code", argv['code'])
                iv = Invitation.use_invitation_code(argv['code'])
            
            login_user(user)

            # token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, current_app.config['SECRET_KEY'], algorithm="HS256")
            # confirm_url = Api.url_for(Api(current_app), resource=UserConfirmController, token=token, _external=True)
            code = user.code
            html = render_template('email.html', code=code)
            subject = "Please confirm your email"
            message = Message(subject=subject, html=html, recipients=[user.username])
            send_email(message)
            user.code = None

            return json.loads(user.to_json())
        except NotUniqueError as e:
            return {'message': e.args }, 400

    # @token_required
# @check_confirmed
    def put(self):
        args = request.args.to_dict()
        updates = request.json
        print(updates)

        user = None

        if 'id' in args:
            user = User.update(args['id'], updates)
        else:
            user = User.update(str(current_user.id), updates)

        if not user:
            return {"message": "User not found id={}".format(args['id'])}, 404

        return json.loads(user.to_json())


    # @token_required
# @check_confirmed
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

        # if check_password_hash(user.password, form['password']):
        #     encoded_jwt = jwt.encode({"some": "payload"}, current_app.config['SECRET_KEY'], algorithm="HS256")
        #     print(encoded_jwt)
        #     token = jwt.encode({'_id': user._id}, current_app.config['SECRET_KEY'], algorithm="HS256")
        login_user(user)
        return json.loads(user.to_json())

        # return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})



class UserConfirmController(Resource):
    def get(self):
        args = request.args.to_dict()
        
        _id = get_field("id", args)
        code = int(get_field("code", args))

        user = User.find_user_by_id(_id)

        if not user:
            return jsonify({'message': 'Account already confirmed. Please login.'})


        if user.confirmed:
            return jsonify({'message': 'Account already confirmed. Please login.'})


        updates = {
            'confirmed': True,
            'confirmed_on': datetime.datetime.utcnow()
        }
        if code == user.code:
            User.update(str(user.id), updates)
            return json.loads(user.to_json())
        return jsonify({'message': 'Not valid code'}), 400


class UserLogoutController(Resource):
    def get(self, args):
        logout_user()
        return json.loads(current_user.to_json())

class UserForgetPwdController(Resource):
    def get(self):
        args = request.args.to_dict()

        code = get_field("code", args)
        username = get_field("username", args)
        pwd = get_field("pwd", args)

        user = User.find_user_by_username(username)

        if code != None and pwd != None:
            code = int(code)
            print(user.code, code)
            if not code == user.code:
                return {'message': 'Code isn\'t correct'}, 401
            user.refresh_token()
            user = User.update(str(user.id), {'password': pwd})
            login_user(user)
            return {'token': user.token}, 200
        elif code != None:
            code = int(code)
            if code != user.code:
                return {'message': 'Code isn\'t correct'}, 401
            return {'message': 'Code is correct'}, 200
        return {'message': 'Some server errors, cheers :)'}, 500

    def post(self):
        args = request.args.to_dict()

        username = args['username']
        user = User.find_user_by_username(username)
        if not user:
            return jsonify({'message': 'User not found'}), 400

        code = generate_code()
        user.code = code
        user.save()

        html = render_template('reset.html', code=code, name=user.name)
        subject = "Restore password"
        message = Message(subject=subject, html=html, recipients=[user.username])
        send_email(message)

        return 200

    
        
