from models.utils.enums import Status
from src.tests.helpers.user import generate_user, generate_admin
from src.utils.roles import Roles


def test_partner(client_user, client_admin, default_moderator):
    user, user_header = generate_user(client_user, role=Roles.user.value)
    data = {
        'request_message': 'Я директор точек сдачи "Второй шанс", хочу '
                           'зарегистрироваться у вас, мои контакты: +792123456',
    }
    resp = client_user.post('/api/partners', headers=user_header, json=data)
    assert resp.status_code == 201, resp.json
    data = resp.json
    assert 'id' in data
    partner_id = data['id']

    # проверяем, что не можем создать токен два раза
    resp = client_user.post('/api/partners', headers=user_header, json=data)
    assert resp.status_code == 400

    # проверяем у админа наличие заявки на создание партнера
    moderator, moderator_header = default_moderator
    resp = client_admin.get(f'/admin/partners/{partner_id}', headers=moderator_header)
    assert resp.status_code == 200, resp.json

    # апрувим заявку
    data = {
        'name': 'Второй шанс',
        'request_message': resp.json['request_message'],
        'status': Status.confirmed.value,
    }
    resp = client_admin.put(f'/admin/partners/{partner_id}', headers=moderator_header, json=data)
    assert resp.status_code == 202, resp.json

    # проверяем, что пользователь стал партнером
    user.reload()
    assert user.role == Roles.partner.value

    # отклоняем заявку
    data['status'] = Status.dismissed.value
    resp = client_admin.put(f'/admin/partners/{partner_id}', headers=moderator_header, json=data)
    assert resp.status_code == 202, resp.json

    # проверяем, что пользователь стал обычным юзером
    user.reload()
    assert user.role == Roles.user.value


def test_create_partner_by_admin(client_user, client_admin, default_moderator):
    user, user_header = generate_user(client_user, role=Roles.user.value)
    moderator, moderator_header = default_moderator

    # создаем партнера
    data = {
        'name': 'Второй шанс',
        'user': str(user.id),
        'request_message': '',
        'status': Status.confirmed.value,
    }
    resp = client_admin.post('/admin/partners', headers=moderator_header, json=data)
    assert resp.status_code == 201, resp.json

    # проверяем, что пользователь стал партнером
    user.reload()
    assert user.role == Roles.partner.value

    # проверяем, что вторую партнерку на этого пользователя повесить нельзя
    resp = client_admin.post('/admin/partners', headers=moderator_header, json=data)
    assert resp.status_code == 400, resp.json
