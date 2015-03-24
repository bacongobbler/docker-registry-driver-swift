# Docker registry swift driver

This is a [docker-registry backend driver][registry-core] for
[Openstack Swift](http://docs.openstack.org/developer/swift/).

[![PyPI version][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]

## Usage

Assuming you have a working docker-registry and swift setup:

```
pip install docker-registry-driver-swift
```

Then edit your docker-registry configuration so that `storage` reads `swift`.


## Options

You may add any of the following to your main docker-registry configuration to further configure it:

```yaml
storage: swift
storage_path: /registry
swift_authurl: _env:OS_AUTH_URL
swift_cacert: _env:OS_CACERT
swift_container: _env:OS_CONTAINER
swift_user: _env:OS_USERNAME
swift_password: _env:OS_PASSWORD
swift_tenant_name: _env:OS_TENANT_NAME
swift_region_name: _env:OS_REGION_NAME
```

## Contributing

Install package dependencies:

```
$ pip install -r requirements.txt
$ pip install -r test/requirements.txt
```

In order to verify what you did is ok, just run `make test`. This will run the tests
provided by [`docker-registry-core`][registry-core].

Please also follow the contributing guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

[pypi-url]: https://pypi.python.org/pypi/docker-registry-driver-swift
[pypi-image]: https://badge.fury.io/py/docker-registry-driver-swift.svg
[registry-core]: https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core
[travis-url]: http://travis-ci.org/bacongobbler/docker-registry-driver-swift
[travis-image]: https://secure.travis-ci.org/bacongobbler/docker-registry-driver-swift.png?branch=master
