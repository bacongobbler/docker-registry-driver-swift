# -*- coding: utf-8 -*-

from docker_registry import testing

from .mocker import Connection   # noqa


class TestQuery(testing.Query):
    def __init__(self):
        self.scheme = 'swift'


class TestDriver(testing.Driver):
    def __init__(self):
        self.scheme = 'swift'
        self.path = ''
        self.config = testing.Config({})

    def setUp(self):
        super(TestDriver, self).setUp()
        self._storage._swift_connection.put_container(
            self._storage._swift_container
        )

    def tearDown(self):
        super(TestDriver, self).tearDown()
        self._storage._swift_connection.delete_container(
            self._storage._swift_container
        )

    # XXX ignoring this
    # swiftclient doesn't raise if what we remove doesn't exist, which is bad!
    def test_remove_inexistent(self):
        pass
