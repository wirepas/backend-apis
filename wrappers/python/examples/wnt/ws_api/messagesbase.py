"""
    MessagesBase
    ============

    Base class for authentication and metadata message classes

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import os
import enum
import json


class MessagesBase(object):
    """Base class for messages classes"""

    class MessageTypes(enum.Enum):
        """Message types enum class"""

        # Authentication server messages
        LOGIN = 1
        LOGOUT = 2

        GET_USERS = 11
        CREATE_USER = 12
        UPDATE_USER = 13
        DELETE_USER = 14

        # Metadata server messages
        GET_BUILDINGS = 1001
        CREATE_BUILDING = 1002
        UPDATE_BUILDING = 1003
        DELETE_BUILDING = 1004

        GET_BUILDINGS_FLOOR_PLANS = 1011
        CREATE_FLOOR_PLAN = 1012
        UPDATE_FLOOR_PLAN = 1013
        DELETE_FLOOR_PLAN = 1014

        GET_FLOOR_PLAN_IMAGE_DATA = 1021
        SET_FLOOR_PLAN_IMAGE_DATA = 1022

        GET_MAP_AREAS = 1031
        CREATE_MAP_AREA = 1032
        UPDATE_MAP_AREA = 1033
        DELETE_MAP_AREA = 1034

        GET_NETWORKS = 1041
        CREATE_NETWORK = 1042
        UPDATE_NETWORK = 1043
        DELETE_NETWORK = 1044

        ADD_NODE_TO_FLOOR_PLAN = 1051
        REMOVE_NODE_FROM_FLOOR_PLAN = 1052

        SET_NODE_METADATA = 1061
        CHANGE_NODE_ID_AND_OR_NETWORK_ID = 1062
        DELETE_NODE = 1063

        SET_NETWORK_DATA = 1071
        SEND_REMOTE_API_REQUEST = 1072
        SEND_DATA_MESSAGE = 1073
        GET_SCRATCHPAD_STATUS = 1074
        SET_OTAP_STATE = 1075
        SET_SCRATCHPAD_ACTION = 1076

        QUERY_COMPONENTS_INFORMATION = 1081

    class ProtocolVersions(enum.Enum):
        """Protocol versions enum class"""

        VERSION_2 = 2
        VERSION_3 = 3
        VERSION_4 = 4
        VERSION_5 = 5

    def __init__(self, logger, protocol_version) -> None:
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        self.logger = logger
        self.protocol_version = protocol_version

    def validate(self, message: dict) -> bool:
        """Validates a message based on the wire protocol version and result

        Args:
            message (dict): a dictionary (json representation)

        Returns:
            bool: True if message validation succeeded. Otherwise throw ValueError exception
        """
        try:
            version = message["version"]
            result = message["result"]

            if version != self.protocol_version:
                raise ValueError

            if result != 1:
                raise ValueError
        except:
            raise ValueError

        return True

    def json_dump_pretty(self, message: dict) -> str:
        """Return formatted JSON message

        Args:
            message (dict): a dictionary (json representation)

        Returns:
            str: Formatted JSON message string
        """
        return os.linesep + json.dumps(message, indent=4, sort_keys=True) + os.linesep
