"""
    Gateway API
    ===========

    This module contains api wrappers to translate protos into
    python objects

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

# flake8: noqa

from .get_configs import *
from .get_gw_info import *
from .set_config import *
from .received_data import *
from .status import *
from .send_data import *
from .upload_scratchpad import *
from .process_scratchpad import *
from .get_scratchpad_status import *
from .gateway_result_code import *
from .otap_helper import *
from .wirepas_exceptions import *
