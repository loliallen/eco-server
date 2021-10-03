import pytest

from src.tests.helpers.user import get_or_create


@pytest.fixture
def client_user():
    from src.app_user import app
    return app.test_client()


@pytest.fixture
def client_admin():
    from src.app_admin import app
    return app.test_client()


@pytest.fixture
def default_moderator():
    from src.app_admin import app
    return get_or_create(app.test_client(), username='admin@exmaple.com')
