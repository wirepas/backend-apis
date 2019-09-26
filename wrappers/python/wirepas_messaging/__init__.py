"""
    WNT
    ===
    Wirepas Network Tool metadata - and realtime situation message definitions

    Metadata message protocol version compatibility
    Version 2: WNT backend 1.7.x
    Version 3: WNT backend 2.0.x

    .. Copyright:
       Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
       See file LICENSE for full license details.
"""

from .__about__ import (
    __author__,
    __author_email__,
    __classifiers__,
    __copyright__,
    __description__,
    __license__,
    __pkg_name__,
    __title__,
    __url__,
    __version__,
    __keywords__,
    __warning_msg__,
)

from . import gateway
from . import nanopb

try:
    from . import wpe
except ImportError as err:
    wpe = "Not available - please compile protos prior to manual install."
    print("Could not import WPE handles ({})".format(err))

try:
    from . import wnt
except ImportError as err:
    wnt = "Not available - please compile protos prior to manual install."
    print("Could not import WPE handles ({})".format(err))

from google.protobuf.internal import api_implementation


# pylint: disable=locally-disabled, protected-access, wrong-import-order
try:
    if api_implementation._default_implementation_type == "python":
        print(__warning_msg__)
except AttributeError:
    print("Could not evaluate protobuf implementation type")


__all__ = [
    "__author__",
    "__author_email__",
    "__classifiers__",
    "__copyright__",
    "__description__",
    "__license__",
    "__pkg_name__",
    "__title__",
    "__url__",
    "__version__",
    "__keywords__",
    "__warning_msg__",
    "gateway",
    "nanopb",
    "wpe",
    "wnt",
]
