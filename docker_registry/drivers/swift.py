import swiftclient

from docker_registry.core import driver
from docker_registry.core import exceptions
from docker_registry.core import lru


class Storage(driver.Base):

    def __init__(self, path=None, config=None):
        self._swift_connection = self._create_swift_connection(config)
        self._swift_container = config.swift_container or 'dev_container'
        self._root_path = config.storage_path or '/'
        if not self._root_path.endswith('/'):
            self._root_path += '/'

    def _create_swift_connection(self, config):
        swift_auth_version = config.swift_auth_version or 2
        return swiftclient.client.Connection(
            authurl=config.swift_authurl,
            cacert=config.swift_cacert,
            user=config.swift_user,
            key=config.swift_password,
            auth_version=swift_auth_version,
            os_options={
                'tenant_name': config.swift_tenant_name,
                'region_name': config.swift_region_name,
                'object_storage_url': config.swift_object_storage_url
            })

    def _init_path(self, path=None):
        path = self._root_path + path if path else self._root_path
        # Openstack does not like paths starting with '/'
        if path:
            if path.startswith('/'):
                path = path[1:]
            if path.endswith('/'):
                path = path[:-1]
        return path

    def _clean_up_name(self, name):
        if self._root_path != '/':
            name = name.replace(
                self._init_path() + '/', '', 1)
        # trim extra trailing slashes
        if name.endswith('/'):
            name = name[:-1]
        return name

    def content_redirect_url(self, path):
        path = self._init_path(path)
        return '/'.join([
            self._swift_connection.url,
            self._swift_container,
            path
        ])

    @lru.get
    def get_content(self, path):
        path = self._init_path(path)
        return self.get_store(path)

    def get_store(self, path, chunk_size=None):
        try:
            _, obj = self._swift_connection.get_object(
                self._swift_container,
                path,
                resp_chunk_size=chunk_size)
            return obj
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    @lru.set
    def put_content(self, path, content):
        path = self._init_path(path)
        self.put_store(path, content)
        return path

    def put_store(self, path, content, chunk=None):
        try:
            self._swift_connection.put_object(self._swift_container,
                                              path,
                                              content,
                                              chunk_size=chunk)
        except Exception:
            raise IOError("Could not put content: %s" % path)

    def stream_read(self, path, bytes_range=None):
        path = self._init_path(path)
        for buf in self.get_store(path, self.buffer_size):
            yield buf

    def stream_write(self, path, fp):
        path = self._init_path(path)
        self.put_store(path, fp, self.buffer_size)

    def head_store(self, path):
        obj = self._swift_connection.head_object(self._swift_container, path)
        return obj

    def list_directory(self, path=None):
        try:
            path = self._init_path(path)
            if path and not path.endswith('/'):
                path += '/'
            _, directory = self._swift_connection.get_container(
                container=self._swift_container,
                prefix=path, delimiter='/')
            if not directory:
                raise
            param = ''
            for inode in directory:
                if 'name' in inode:
                    param = 'name'
                elif 'subdir' in inode:
                    param = 'subdir'
                else:
                    raise
                # trim extra trailing slashes
                yield self._clean_up_name(inode[param])
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def exists(self, path):
        path = self._init_path(path)
        try:
            self.head_store(path)
            return True
        except Exception:
            return False

    @lru.remove
    def remove(self, path):
        path = self._init_path(path)
        try:
            self._swift_connection.delete_object(self._swift_container, path)
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def get_size(self, path):
        path = self._init_path(path)
        try:
            headers = self.head_store(path)
            return headers['content-length']
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)
