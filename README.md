# Docker registry swift driver

This is a [docker-registry backend driver](https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core) based on the [Swift](https://swiftstack.com/) storage.

[![PyPI version][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]

## Usage

Assuming you have a working docker-registry and swift setup.

`pip install docker-registry-driver-swift`

Then edit your docker-registry configuration so that `storage` reads `swift`.


## Options

You may add any of the following to your main docker-registry configuration to further configure it.


1.    `storage_path`: /
1.    `swift_container`: 'dev_container'
1.    `swift_auth_version`: 2
1.    `swift_authurl`
1.    `swift_user`
1.    `swift_password`
1.    `swift_tenant_name`
1.    `swift_region_name`


Example:

```yaml
storage: swift
storage_path: /registry
swift_authurl: _env:OS_AUTH_URL
swift_container: _env:OS_CONTAINER
swift_user: _env:OS_USERNAME
swift_password: _env:OS_PASSWORD
swift_tenant_name: _env:OS_TENANT_NAME
swift_region_name: _env:OS_REGION_NAME
```

## Developer setup

Clone this.

Optionnally [install swift](http://docs.openstack.org/developer/swift/howto_installmultinode.html) (rely on the mock otherwise):

Get your python ready:

```
sudo apt-get install python-pip
sudo pip install tox
```

Install the python-swiftclient globally:

`pip install python-swiftclient`

You are ready to hack.
In order to verify what you did is ok, just run `tox`.

This will run the tests provided by [`docker-registry-core`](https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core)


## Developer setup caveats

### "Why do I need to install swiftclient globally?"

Because openstack uses a packaging technology ([pbr](http://docs.openstack.org/developer/pbr/)) that breaks miserably when trying to use pip with --egg (in the tox / venv context)

### "Why do we need to use pip with --egg?"

Because python namespaces are broken. Or maybe pip is. Or maybe you read and make your own idea about it :-)

 * https://github.com/pypa/pip/issues/3#issuecomment-1659959
 * http://stackoverflow.com/questions/17338925/cannot-install-two-packages-that-use-the-same-namespace

## License

This is licensed under the Apache license.
Most of the code here comes from docker-registry, under an Apache license as well.

[pypi-url]: https://pypi.python.org/pypi/docker-registry-driver-swift
[pypi-image]: https://badge.fury.io/py/docker-registry-driver-swift.svg

[travis-url]: http://travis-ci.org/bacongobbler/docker-registry-driver-swift
[travis-image]: https://secure.travis-ci.org/bacongobbler/docker-registry-driver-swift.png?branch=master
