# -*- coding: utf-8 -*-

from docker_registry.testing import Driver
from docker_registry.testing import Query
from docker_registry.testing.utils import Config
import docker_registry.drivers.swift as driverspace

from .mocker import Connection   # noqa


class TestQuery(Query):
    def __init__(self):
        self.scheme = 'swift'
        self.cls = driverspace


class TestDriver(Driver):
    def __init__(self):
        self.scheme = 'swift'
        self.path = ''
        self.config = Config({'swift_container': 'testcontainer'})
        # self.path = 'tmp/storagetest'

    def setUp(self):
        super(TestDriver, self).setUp()
        self._storage._swift_connection.put_container(
            self._storage._swift_container
        )

    def tearDown(self):
        self._storage._swift_connection.delete_container(
            self._storage._swift_container
        )

    # XXX ignoring this
    # swiftclient doesn't raise if what we remove doesn't exist
    def test_remove_inexistent(self):
        pass
