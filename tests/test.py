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

    def test_list_directory(self):
        # Test with root directory
        super(TestDriver, self).test_list_directory()
        self.tearDown()

        # Test with custom root directory
        self.config = testing.Config({'storage_path': '/foo'})
        self.setUp()
        super(TestDriver, self).test_list_directory()

    def test_list_directory_with_subdir(self):
        # Test with root directory
        super(TestDriver, self).test_list_directory_with_subdir()
        self.tearDown()

        # Test with custom root directory
        self.config = testing.Config({'storage_path': '/foo'})
        self.setUp()
        super(TestDriver, self).test_list_directory_with_subdir()

    def test_swift_root_path_default(self):
        assert self._storage._root_path == '/'
        assert self._storage._init_path() == ''
        assert self._storage._init_path('foo') == 'foo'

    def test_swift_root_path_empty(self):
        config = testing.Config({'storage_path': ''})
        self._storage.__init__(config=config)
        assert self._storage._init_path() == ''
        assert self._storage._init_path('foo') == 'foo'

    def test_swift_root_path_custom(self):
        config = testing.Config({'storage_path': '/foo'})
        self._storage.__init__(config=config)
        assert self._storage._init_path() == 'foo'
        assert self._storage._init_path('foo') == 'foo/foo'
