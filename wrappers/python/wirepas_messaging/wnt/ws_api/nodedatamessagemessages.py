# pylint: disable=duplicate-code
"""
    Node data message messages
    ==========================

    Node data message related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class NodeDataMessages(AuthenticationMessages):
    """This class generates and decodes node data message related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(NodeDataMessages, self).__init__(logger, protocol_version)

    def message_send_node_data_message(
        self,
        node_id: int,
        network_id: int,
        sink_node_id: int,
        source_end_point: int,
        destination_end_point: int,
        qos: int,
        payload: str,
    ) -> dict:
        """Returns send node data message metadata message

        Args:
            node_id (int): node id
            network_id (int): node's network id
            sink_node_id (int): node's sink's id
            source_end_point (int): message source end point
            destination_end_point (int): message destination end point
            qos (int): message quality of service level
            payload (str): hexadecimal payload
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.SEND_DATA_MESSAGE.value,
            data=dict(
                command=dict(
                    node_id=node_id,
                    network_id=network_id,
                    sink_node_id=sink_node_id,
                    source_end_point=source_end_point,
                    destination_end_point=destination_end_point,
                    qos=qos,
                    payload=payload,
                ),
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_send_node_data_message(self, message: dict) -> bool:
        """Parses send node data message response

        Args:
            message (dict): send node data message response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot send node data message")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
