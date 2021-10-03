from src.models.user.UserModel import User
from src.tests.factory.user import UserModelFactory
from src.utils.roles import Roles


def generate_user(client_user, password='SuperPassword1234', **kwargs):
    user = UserModelFactory(password_=password, **kwargs)
    resp = client_user.post('api/login', data={'username': user.username, 'password': password})
    assert resp.status_code == 200
    return user, {'Authorization': 'Bearer ' + resp.json['access_token']}


def generate_admin(client_admin, password='SuperPassword1234', role=Roles.moderator.value, **kwargs):
    admin = UserModelFactory(password_=password, role=role, **kwargs)
    resp = client_admin.post('admin/login', data={'username': admin.username, 'password': password})
    assert resp.status_code == 200
    return admin, {'Authorization': 'Bearer ' + resp.json['access_token']}


def get_or_create(client_admin, username, password='SuperPassword1234', role=Roles.moderator.value, **kwargs):
    resp = client_admin.post('admin/login', data={'username': username, 'password': password})
    if resp.status_code == 404:
        return generate_admin(client_admin, password, role, username=username)
    assert resp.status_code == 200
    admin = User.objects.filter(username=username).first()
    return admin, {'Authorization': 'Bearer ' + resp.json['access_token']}
