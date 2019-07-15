# Wirepas Oy

from . import gateway
from . import nanopb

try:
    from . import wpe
except ImportError:
    print("Could not import WPE handles")

try:
    from . import wnt
except ImportError:
    print("Could not import WPE handles")


from google.protobuf.internal import api_implementation

warning_msg = """
***********************************************************************
* WARNING:
*     You are using the pure python protobuf implementation.
*     For better results, please consider using the cpp version.
*     For more information please consult:
*     https://github.com/protocolbuffers/protobuf/tree/master/python
***********************************************************************
"""

if api_implementation._default_implementation_type == "python":
    print(warning_msg)
