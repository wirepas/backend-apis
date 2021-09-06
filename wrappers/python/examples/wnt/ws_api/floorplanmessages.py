# pylint: disable=duplicate-code
"""
    Floor Plans
    ===========

    Floor plans related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class FloorPlanMessages(AuthenticationMessages):
    """This class generates and decodes floor plans related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(FloorPlanMessages, self).__init__(logger, protocol_version)

        self.image_id = None
        self.image_data_base64 = None
        self.new_floor_plan_id = None

    def message_create_floor_plan(self, building_id: str, floor_plan_name: str) -> dict:
        """Returns floor plan creation message

        Args:
            building_id (str): building id of the building that the floor plan is linked to
            floor_plan_name (str): new floor plan name
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_FLOOR_PLAN.value,
            data=dict(
                buildings=[
                    dict(
                        id=building_id,
                        floor_plans=[
                            dict(
                                name=floor_plan_name,
                                latitude_lefttop=None,
                                longitude_lefttop=None,
                                altitude_lefttop=None,
                                x_normcoord_lefttop=0,
                                y_normcoord_lefttop=0,
                                latitude_righttop=None,
                                longitude_righttop=None,
                                altitude_righttop=None,
                                x_normcoord_righttop=1,
                                y_normcoord_righttop=0,
                                latitude_leftbottom=None,
                                longitude_leftbottom=None,
                                altitude_leftbottom=None,
                                x_normcoord_leftbottom=0,
                                y_normcoord_leftbottom=1,
                                latitude_rightbottom=None,
                                longitude_rightbottom=None,
                                altitude_rightbottom=None,
                                x_normcoord_rightbottom=1,
                                y_normcoord_rightbottom=1,
                                x_distance_point1=0.3,
                                y_distance_point1=0.5,
                                x_distance_point2=0.7,
                                y_distance_point2=0.5,
                                distance_in_m=1,
                                level=0,
                            )
                        ],
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        if self.protocol_version >= self.ProtocolVersions.VERSION_3.value:
            floor_plan = message["data"]["buildings"][0]["floor_plans"][0]
            floor_plan["image_width"] = 1
            floor_plan["image_height"] = 1

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_create_floor_plan(self, message: dict) -> bool:
        """Parses create floor plan response, and stores new floor plan id

        Args:
            message (dict): the create floor plan response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot create floor plan")
            self.logger.error(self.json_dump_pretty(message))
            return False

        data = message["data"]

        self.new_floor_plan_id = data["buildings"][0]["floor_plans"][0]["id"]

        return True

    def message_update_floor_plan(self, floor_plan_id: str, **kwargs: dict) -> dict:
        """Returns floor plan update message

        Args:
            floor_plan_id (str): updated floor plan
            kwargs (dict): parameters dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_FLOOR_PLAN.value,
            data=dict(
                buildings=[
                    dict(
                        floor_plans=[
                            dict(
                                # Floor plan id is the only required field
                                id=floor_plan_id
                            )
                        ]
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        message["data"]["buildings"][0]["floor_plans"][0].update(kwargs)

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_update_floor_plan(self, message: dict) -> bool:
        """Parses update floor plan response

        Args:
            message (dict): the update floor plan response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot update floor plan")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_get_floor_plans(self, building_id: str) -> dict:
        """
        Returns get floor plans message

        Args:
            building_id (str): Id of building whose floor plans are fetched

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_BUILDINGS_FLOOR_PLANS.value,
            data=dict(
                buildings=[dict(id=building_id)],
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_get_floor_plans(self, message: dict) -> bool:
        """Parses get floor plans response

        Args:
            message (dict): the get floor plans response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot get floor plans")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_delete_floor_plan(self, floor_plan_id: str) -> dict:
        """Returns floor plan deletion message

        Args:
            floor_plan_id (str): floor plan id

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_FLOOR_PLAN.value,
            data=dict(
                buildings=[dict(floor_plans=[dict(id=floor_plan_id)])],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_delete_floor_plan(self, message: dict) -> bool:
        """Parses delete floor plan response

        Args:
            message (dict): the delete floor plan response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot delete floor plan")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_get_image(self, image_id: str) -> dict:
        """Returns floor plan image getting message

        Args:
            image_id (str): image id
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_FLOOR_PLAN_IMAGE_DATA.value,
            data=dict(image_id=image_id),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_get_image(self, message: dict) -> bool:
        """Parses get image response, and stores the image data

        Args:
            message (dict): the get image response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot get image")
            self.logger.error(self.json_dump_pretty(message))
            return False

        data = message["data"]

        self.image_data_base64 = data["image_base64"]

        return True

    def message_set_image(self, image_data_base64: str) -> dict:
        """Returns floor plan image setting message

        Args:
            image_data_base64 (str): image binary data with Base64 encoding
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.SET_FLOOR_PLAN_IMAGE_DATA.value,
            data=dict(
                image_base64=image_data_base64, originator_token=self.originator_token
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_set_image(self, message: dict) -> bool:
        """Parses set image response, and stores new image id

        Args:
            message (dict): the set image response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot set image")
            self.logger.error(self.json_dump_pretty(message))
            return False

        data = message["data"]

        self.image_id = data["image_id"]

        return True
