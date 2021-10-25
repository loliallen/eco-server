import re
from unittest.mock import patch

from src.tests.helpers.user import generate_user
from src.utils.roles import Roles


@patch('src.send_email.mail.send')
def test_recovery(send, client_user):
    user, user_header = generate_user(client_user, role=Roles.user.value)

    resp = client_user.post('/api/send_check_code', json={'username': 'not email'})
    assert resp.status_code == 404

    with client_user.application.app_context():
        resp = client_user.post('/api/send_check_code', json={'username': user['username']})
        assert resp.status_code == 200
        code = re.findall(r'\d{6}', send.call_args_list[0][0][0].html)[0]

    resp = client_user.post('/api/send_check_code', json={'username': user['username']})
    assert resp.status_code == 400

    resp = client_user.post('/api/get_recovery_token', json={'username': user['username'], 'code': 'wrong code'})
    assert resp.status_code == 400

    resp = client_user.post('/api/get_recovery_token', json={'username': user['username'], 'code': code})
    assert resp.status_code == 200
    assert 'recovery_token' in resp.json
    recovery_token = resp.json['recovery_token']

    new_pass = {'password': 'Password12345', 'password_repeat': 'Password12345'}
    resp = client_user.post('/api/change_password', json=new_pass, headers=user_header)
    assert resp.status_code == 405

    resp = client_user.post('/api/change_password', json=new_pass,
                            headers={'Authorization': 'Bearer ' + recovery_token})
    assert resp.status_code == 200
