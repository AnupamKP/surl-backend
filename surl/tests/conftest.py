import pytest
from surl.app import create_app
from surl.utils.db import db as _db


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app(env='local')

    with _app.app_context():
        yield _app


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()


@pytest.fixture(scope='session')
def db(app):
    #_db.drop_all(app=app)
    #_db.create_all(app=app)

    return _db



