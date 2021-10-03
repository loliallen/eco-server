import re
from unittest.mock import patch

from src.tests.factory.user import UserFactory


@patch('src.send_email.mail.send')
def test_register(send, client_user):
    user: dict = UserFactory()
    code = None
    with client_user.application.app_context():
        resp = client_user.post('/api/register', data=user)
        code = re.findall(r'\d{6}', send.call_args_list[0][0][0].html)[0]
    assert resp.status_code == 201, f'{resp.json} [{user}]'

    resp = client_user.post('/api/confirm', data={'username': user['username'],
                                                  'code': code})
    assert resp.status_code == 200
    assert resp.json == {'status': 'success'}

    resp = client_user.post('/api/login', data=user)
    assert resp.status_code == 200
    assert 'access_token' in resp.json
