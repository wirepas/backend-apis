# pylint: disable=duplicate-code
"""
    Buildings
    =========

    Buildings related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class BuildingMessages(AuthenticationMessages):
    """This class generates and decodes buildings related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(BuildingMessages, self).__init__(logger, protocol_version)

        self.new_building_id = None

    def message_create_building(self, building_name: str) -> dict:
        """Returns building creation message

        Args:
            building_name (str): new building name
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_BUILDING.value,
            data=dict(
                buildings=[dict(name=building_name)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_create_building(self, message: dict) -> bool:
        """Parses create building response, and stores new building id

        Args:
            message (dict): the create building response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot create building")
            self.logger.error(self.json_dump_pretty(message))
            return False

        data = message["data"]

        self.new_building_id = data["buildings"][0]["id"]

        return True

    def message_update_building(self, building_id: str, building_name: str) -> dict:
        """Returns building update message

        Args:
            building_id (str): building id
            building_name (str): new building name

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_BUILDING.value,
            data=dict(
                buildings=[dict(id=building_id, name=building_name)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_update_building(self, message: dict) -> bool:
        """Parses update building response

        Args:
            message (dict): the update building response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot update building")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_get_buildings(self) -> dict:
        """
        Returns get buildings message

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_BUILDINGS.value,
            data=dict(),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_get_buildings(self, message: dict) -> bool:
        """Parses get buildings response

        Args:
            message (dict): the get buildings response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot get buildings")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_delete_building(self, building_id: str) -> dict:
        """Returns building deletion message

        Args:
            building_id (str): building id

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_BUILDING.value,
            data=dict(
                buildings=[dict(id=building_id)], originator_token=self.originator_token
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_delete_building(self, message: dict) -> bool:
        """Parses delete building response

        Args:
            message (dict): the delete building response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot delete building")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
