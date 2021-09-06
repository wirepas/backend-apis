# pylint: disable=duplicate-code
"""
    Nodes
    =====

    Node related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class NodeMessages(AuthenticationMessages):
    """This class generates and decodes node related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(NodeMessages, self).__init__(logger, protocol_version)

    def message_set_node_metadata(
        self,
        node_id: int,
        network_id: int,
        name: str,
        description: str,
        latitude: float,
        longitude: float,
        altitude: float,
        is_approved: bool,
        is_virtual: bool,
        is_anchor: bool,
    ) -> dict:
        """Returns set node metadata message

        Args:
            node_id (int): node id
            network_id (int): node's network id
            name (str): name for the node
            description (str): description for the node
            latitude (float): node's latitude
            longitude (float): node's longitude
            altitude (float): node's altitude
            is_approved (bool): is node approved
            is_virtual (bool): is node used for planning
            is_anchor (bool): is node an anchor in positioning use case
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.SET_NODE_METADATA.value,
            data=dict(
                nodes=[
                    dict(
                        id=node_id,
                        network_id=network_id,
                        name=name,
                        description=description,
                        latitude=latitude,
                        longitude=longitude,
                        altitude=altitude,
                        is_approved=is_approved,
                        is_virtual=is_virtual,
                        is_anchor=is_anchor,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        if self.protocol_version == self.ProtocolVersions.VERSION_2.value:
            node = message["data"]["nodes"][0]
            node["pixel_location_x"] = -1
            node["pixel_location_y"] = -1

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_set_node_metadata(self, message: dict) -> bool:
        """Parses set node metadata response

        Args:
            message (dict): set node metadata response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot set node metadata")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_add_node_to_floor_plan(
        self, node_id: int, network_id: int, floor_plan_id: str
    ) -> dict:
        """Returns set node metadata message

        Args:
            node_id (int): node id
            network_id (int): node's network id
            floor_plan_id (str): id of the floor plan where node is placed
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.ADD_NODE_TO_FLOOR_PLAN.value,
            data=dict(
                nodes=[
                    dict(id=node_id, network_id=network_id, floor_plan_id=floor_plan_id)
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_add_node_to_floor_plan(self, message: dict) -> bool:
        """Parses add node to floor plan response

        Args:
            message (dict): add node to floor plan response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot add node to floor plan")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_remove_node_from_floor_plan(
        self, node_id: int, network_id: int
    ) -> dict:
        """Returns remove node from floor plan message

        Args:
            node_id (int): node id
            network_id (int): node's network id
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.REMOVE_NODE_FROM_FLOOR_PLAN.value,
            data=dict(
                nodes=[dict(id=node_id, network_id=network_id)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_remove_node_from_floor_plan(self, message: dict) -> bool:
        """Parses remove node from floor plan response

        Args:
            message (dict): remove node from floor plan response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot remove node from floor plan")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_delete_node(self, node_id: int, network_id: int) -> dict:
        """Returns delete node message

        Args:
            node_id (int): node id
            network_id (int): node's network id
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_NODE.value,
            data=dict(
                nodes=[dict(id=node_id, network_id=network_id)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_delete_node(self, message: dict) -> bool:
        """Parses delete node response

        Args:
            message (dict): delete node response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot delete node")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
