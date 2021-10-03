from src.tests.factory.rec_point import RecPointModelFactory, FilterModelFactory
from src.tests.helpers.user import generate_user
from src.utils.roles import Roles


def test_recycle(client_user, client_admin):
    # проверка положительного сценарий сдачи отходов в пункт приема
    filters = [FilterModelFactory(), FilterModelFactory()]
    rec_point = RecPointModelFactory()
    rec_point.accept_types = [i.id for i in filters]
    rec_point.save()

    user, user_header = generate_user(client_user, role=Roles.user.value)
    admin_pp, admin_pp_header = generate_user(
        client_user,
        role=Roles.admin_pp.value,
        attached_rec_point=str(rec_point.id)
    )

    data = {
        'user_token': user.token,
        'items': [
            {
                'filter_type': str(filters[0].id),
                'amount': 1
            }
        ]
    }
    resp = client_user.post('/api/recycle', headers=admin_pp_header, json=data)
    assert resp.status_code == 200, resp.json

    # approve
    # moderator, moderator_header = generate_admin(client_admin)


