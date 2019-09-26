"""
    Gateway result code
    ===================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

# flake8: noqa

import enum
from ..otap_message_pb2 import *


class ScratchpadType(enum.Enum):
    SCRATCHPAD_TYPE_BLANK = BLANK
    SCRATCHPAD_TYPE_PRESENT = PRESENT
    SCRATCHPAD_TYPE_PROCESS = PROCESS


class ScratchpadStatus(enum.Enum):
    SCRATCHPAD_STATUS_SUCCESS = SUCCESS
    SCRATCHPAD_STATUS_NEW = NEW
    SCRATCHPAD_STATUS_ERROR = ERROR


def parse_scratchpad_info(message_obj, dic):
    dic["len"] = message_obj.len
    dic["crc"] = message_obj.crc
    dic["seq"] = message_obj.seq


def set_scratchpad_info(message_obj, dic):
    message_obj.len = dic["len"]
    message_obj.crc = dic["crc"]
    message_obj.seq = dic["seq"]
