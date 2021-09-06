# pylint: disable=duplicate-code
"""
    Areas
    =====

    Area related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class AreaMessages(AuthenticationMessages):
    """This class generates and decodes area related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(AreaMessages, self).__init__(logger, protocol_version)

        self.new_area_id = None

    def message_get_floor_plan_areas(self, floor_plan_id: str) -> dict:
        """Returns get floor plan areas message

        Args:
            floor_plan_id (str): floor plan id
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_MAP_AREAS.value,
            data=dict(
                buildings=[dict(floor_plans=[dict(id=floor_plan_id)])],
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_get_floor_plan_areas(self, message: dict) -> bool:
        """Parses get floor plan areas response

        Args:
            message (dict): the get floor plans area response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot query areas")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_create_area(self, floor_plan_id: str, area_name: str) -> dict:
        """Returns area creation message

        Args:
            floor_plan_id (str): floor plan id where area is created
            area_name (str): new area name
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_MAP_AREA.value,
            data=dict(
                buildings=[
                    dict(
                        floor_plans=[
                            dict(
                                id=floor_plan_id,
                                areas=[
                                    dict(name=area_name, a=0, r=0, g=0, b=0, llas=[])
                                ],
                            )
                        ]
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_create_area(self, message: dict) -> bool:
        """Parses create area response, and stores new area id

        Args:
            message (dict): the create area response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot create area")
            self.logger.error(self.json_dump_pretty(message))
            return False

        data = message["data"]

        self.new_area_id = data["buildings"][0]["floor_plans"][0]["areas"][0]["id"]

        return True

    def message_update_area(
        self,
        area_id: str,
        floor_plan_id: str,
        area_name: str,
        color_a: int,
        color_r: int,
        color_g: int,
        color_b: int,
        llas: [],
    ) -> dict:
        """Returns area update message

        Args:
            area_id (str): area id
            floor_plan_id (str): floor plan id
            area_name (str): area name
            color_a (int): area color alpha (0-255)
            color_r (int): area color red (0-255)
            color_g (int): area color green (0-255)
            color_b (int): area color blue (0-255)
            llas ([]): array of latitude, longitude and altitude dictionaries for area corner points
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_MAP_AREA.value,
            data=dict(
                buildings=[
                    dict(
                        floor_plans=[
                            dict(
                                id=floor_plan_id,
                                areas=[
                                    dict(
                                        id=area_id,
                                        name=area_name,
                                        a=color_a,
                                        r=color_r,
                                        g=color_g,
                                        b=color_b,
                                        llas=llas,
                                    )
                                ],
                            )
                        ]
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_update_area(self, message: dict) -> bool:
        """Parses update area response

        Args:
            message (dict): the update area response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot update area")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_delete_area(self, floor_plan_id: str, area_id: str) -> dict:
        """Returns area delete message

        Args:
            floor_plan_id (str): floor plan id
            area_id (str): area id
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_MAP_AREA.value,
            data=dict(
                buildings=[
                    dict(floor_plans=[dict(id=floor_plan_id, areas=[dict(id=area_id)])])
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_delete_area(self, message: dict) -> bool:
        """Parses delete area response

        Args:
            message (dict): the delete area response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot delete area")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
