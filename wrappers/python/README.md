# Wirepas Messaging

![PyPI](https://img.shields.io/pypi/v/wirepas-messaging.svg?label=wirepas-messaging)

This wheel contains the generated code to interact with Wirepas Mesh services.

## Installation

To install the wirepas messaging package start by cloning the repo

```shell
    git clone git@github.com:wirepas/backend-apis.git
```

Change directory to backend-apis/wrappers/python and create the wheel and
tar files with

```shell
    ./utils/generate_whell.sh
```

Afterwards, install the package from the dist folder with

```shell
    python install dist/wirepas_messaging-*.whl
```
or

```shell
    python install dist/wirepas_messaging-*.tar
```
For development mode installation use

```shell
    pip install -e .
```

## Install from PyPi

This package is available from [PyPi][pypi].

## License

Licensed under the Apache License, Version 2.0. See LICENSE for the full
license text.

[pypi]: https://pypi.org/project/wirepas-messaging/
