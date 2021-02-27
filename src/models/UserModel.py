from mongoengine import Document, StringField, QuerySet, BooleanField, DateTimeField, IntField
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
from datetime import datetime
from flask_login import UserMixin
from src.utils.generator import random_string, generate_code
from src.utils.qrcodes import create_qr_code 


REL_PATH = "/static/users"
files_storage = Path('./src'+REL_PATH)


class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    name = StringField(required=True)
    surname = StringField()
    password = StringField(required=True)
    image = StringField()
    confirmed = BooleanField(default=False)
    confirmed_on = DateTimeField()
    eco_coins = IntField(default=0)

    code = IntField(default=generate_code)
    qrcode = StringField()

    token = StringField(default=random_string)
    
    meta = {
        "db_alias": "core",
        "collection": "users"
    }
    def refresh_token(self):
        self.token = random_string()
        self.save()


def read() -> QuerySet:
    users = User.objects.all()
    return users


def get_one_user(user_id: str) -> User:
    user = User.objects(id=user_id).exclude('password').first()

    if not user:
        return None

    return user


def create(obj: dict, image: str) -> User:
    obj['password'] = generate_password_hash(obj['password'], method='sha256')
    user = User(**obj)
    
    user.qrcode = create_qr_code(user.token)
    
    if image != "":
        image = REL_PATH + "/" + image
    user.image = image
    user.save()

    return user


def update(user_id: str, updates:object) -> User:
    user = find_user_by_id(user_id)
    print(user)

    if not user:
        return None

    user.update(**updates)
    if "password" in updates:
        user.password = generate_password_hash(user.password, method='sha256')
    user.save()

    return user


def delete(user_id) -> User:
    user = find_user_by_id(user_id)

    if not user:
        return None

    user.delete()

    return user


def find_user_by_id(user_id:str) -> User:
    user = None
    user = User.objects(id=user_id).first()

    return user


def find_user_by_username(username:str) -> User:
    user = None
    user = User.objects(username=username).first()

    return user


def check_password(user: User, password: str) -> bool:
    return check_password_hash(user.password, password)