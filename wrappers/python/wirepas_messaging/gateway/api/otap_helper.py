# Copyright Wirepas Ltd 2019

import wirepas_messaging
from ..otap_message_pb2 import *
import enum


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
