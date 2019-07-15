# Wirepas Messaging

![PyPI](https://img.shields.io/pypi/v/wirepas-messaging.svg?label=wirepas-messaging)

This wheel contains the generated code to interact with Wirepas Mesh services.

## Installation

To install the wirepas messaging package start by cloning the repo

```shell
    git clone https://github.com/wirepas/backend-apis.git
```

Install the protocol buffer compiler, eg,

```shell
   pip install grpcio-tools
```

Copy and compile the protocol buffer files

```shell
    ./utils/pull_protos.sh
    ./utils/compile_protos.sh
```

Generate the python wheel with

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
