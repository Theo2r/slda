import warnings
import os
import string

import pytest
from bddrest import Given, status, response

import slda


warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def app():
    app = slda.app
    app.ready()
    yield app
    app.shutdown()


@pytest.fixture
def urandommock():
    backup = os.urandom
    os.urandom = lambda c: string.ascii_letters.encode()[:c]
    yield
    os.urandom = backup


@pytest.fixture
def redis():

    class RedisMock:
        def __init__(self):
            self.maindict = dict()

        def get(self, key):
            return self.maindict.get(key, '').encode()

        def set(self, key, value):
            self.maindict[key] = value

        def setnx(self, key: str, value):
            if not self.maindict.get(key):
                self.set(key, value)
                return 1
            return 0

        def flushdb(self):
            self.maindict.clear()

    backup = slda.redis
    slda.redis = RedisMock()
    yield slda.redis
    slda.redis = backup


def test_urlpost(app, redis, urandommock):
    app.ready()

    with Given(
        title='Creating a new url',
        application=app,
        url='/apiv1/urls',
        verb='POST',
        json=dict(url='http://example.com')
    ):
        assert status == 201
        assert response.json['id'] == 'LJO1vnZOE4'
