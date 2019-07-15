# Wirepas Oy

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

try:
    from . import gateway
    from . import nanopb
except ImportError:
    print("Could not import gateway api wrapper")

try:
    from . import wpe
except ImportError:
    print("Could not import WPE handles")

try:
    from . import wnt
except ImportError:
    print("Could not import WPE handles")

try:
    from google.protobuf.internal import api_implementation

    if api_implementation._default_implementation_type == "python":
        print(__warning_msg__)
except ImportError:
    print("Could not import api_implementation from google.protobuf.internal")
