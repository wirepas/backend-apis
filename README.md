# Backend APIs

[![Build Status](https://travis-ci.com/wirepas/backend-apis.svg?branch=master)](https://travis-ci.com/wirepas/backend-apis)

This repository contains the message definition files for the Wirepas'
service APIs, specifically:

- [Wirepas Gateway][here_gateway]
- [Wirepas Network Tool][here_wnt]
- [Wirepas Positioning Engine][here_wpe]

In addition to the the message specification files, the repository contains language specific wrappers (classes, function, ...) that simplify the translation of the API data into a target language object (see Figure 1).

![runtime operation of wm-config][here_docs_operation]

**Figure 1 -** Illustration of messaging wrapper's function within applications.

## Language wrappers

- **Python**: wirepas_messaging \[[source][here_python]\] \[[PyPi][pypi_messaging]\] \[[docs][here_python_docs]\]

## Wirepas Network Tool Git tag correspondence

| WNT version   | Tag           |
| ------------- |:-------------:|
| v2.0.0        | v1.3.0        |
| v3.0.0        | v1.4.0        |

## Contributing

We welcome your contributions!

Please read the [instructions on how to do it][here_contribution]
and please review our [code of conduct][here_code_of_conduct].

## License

Licensed under the Apache License, Version 2.0.
See [LICENSE][here_license] for the full license text.

[here_python]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python
[here_python_docs]: https://backend-apis.readthedocs.io/en/latest/index.html

[here_docs_operation]: ./docs/img/overview.png

[here_gateway]: ./gateway_to_backend

[here_wpe]: ./wpe

[here_wnt]: ./wnt

[pypi_messaging]: https://pypi.org/project/wirepas-messaging/

[here_code_of_conduct]: https://github.com/wirepas/backend-apis/blob/master/CODE_OF_CONDUCT.md

[here_contribution]: https://github.com/wirepas/backend-apis/blob/master/CONTRIBUTING.md

[here_license]: https://github.com/wirepas/backend-apis/blob/master/LICENSE
