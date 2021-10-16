from src.tests.factory.rec_point import RecPointModelFactory, FilterFactory


def test_get_filters(client_user):
    resp = client_user.get('/api/filters')
    assert resp.status_code == 200


def test_add_new_filter(client_user, client_admin, default_moderator):
    # проверяем дотсупность фильтров модератором
    moderator, moderator_headers = default_moderator
    resp = client_admin.get('/admin/filters', headers=moderator_headers)
    assert resp.status_code == 200

    # создаем фильтров модератором
    filter_ = FilterFactory()
    resp = client_admin.post('/admin/filters', headers=moderator_headers, json=filter_)
    assert resp.status_code == 201

    # проверяем доступность созданного фильтра модератором
    resp = client_admin.get(f'/admin/filters/{resp.json["id"]}', headers=moderator_headers)
    assert resp.status_code == 200
    filter_['id'] = resp.json['id']
    assert filter_ == resp.json

    # проверяем что фильтр появился у пользователей
    resp = client_user.get(f'/api/filters')
    assert resp.status_code == 200
    filter_.pop('visible')
    assert filter_ in resp.json


def test_get_rec_points(client_user):
    position = [55.799779, 49.1319283]
    radius = 10

    RecPointModelFactory(coords=position)

    # без параметром запрос не проходит
    resp = client_user.get('/api/rec_points')
    assert resp.status_code == 400

    # запрос с пагинацией + точка вокруг которой в радиусе n метров проиходит поиск
    resp = client_user.get('/api/rec_points', query_string={'position': str(position), 'radius': radius,
                                                            'page': 1, 'size': 10})
    assert resp.status_code == 200
    assert len(resp.json['data']) >= 1
    assert ['id', 'name', 'partner', 'partner_name', 'payback_type',
            'reception_type', 'work_time', 'address', 'contacts', 'accept_types_names',
            'accept_types', 'coords', 'description', 'getBonus', "images", "external_images",
            "approve_status"] == list(resp.json['data'][0].keys())

    # запрос без пагинации - урезанные данные по каждому пункту
    resp = client_user.get('/api/rec_points', query_string={'position': str(position), 'radius': radius})
    assert resp.status_code == 200
    assert len(resp.json) >= 1
    assert ['id', 'name', 'payback_type', 'reception_type',
            'accept_types_names', 'accept_types', 'coords'] == list(resp.json[0].keys())


