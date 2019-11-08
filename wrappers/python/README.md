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
    ./utils/generate_wheel.sh
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

If you wish to run the examples, please install with the extra requirements

```shell
    python install dist/wirepas_messaging-*.whl[examples]
```

## Services API documentation

Please refer to the [backend apis repository][github_backend_apis] for
documentation on the Wirepas' services APIs.

## Examples

For more information about Wirepas Network Tool examples please see
[README.md][wnt_examples_readme]

## Install from PyPi

This package is available from [PyPi][pypi].

## License

Licensed under the Apache License, Version 2.0.
See [LICENSE][here_license] for the full license text.

[pypi]: https://pypi.org/project/wirepas-messaging/

[wnt_examples_readme]: https://github.com/wirepas/backend-apis/blob/master/wrappers/python/examples/wnt/README.md

[github_backend_apis]: https://github.com/wirepas/backend-apis

[here_license]: https://github.com/wirepas/backend-apis/blob/master/wrappers/python/LICENSE
