# pylint: disable=duplicate-code
"""
    Floor plan example
    ==================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from utils import get_settings, setup_log
from connections import Connections
from filehelper import FileHelper

import os
import json

from enum import Enum, auto
from wirepas_messaging.wnt.ws_api import BuildingMessages, FloorPlanMessages


class Messages(BuildingMessages, FloorPlanMessages):
    """Aggregation class for messages"""

    def __init__(self, logger, protocol_version) -> None:
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        BuildingMessages.__init__(self, logger, protocol_version)
        FloorPlanMessages.__init__(self, logger, protocol_version)


class FloorPlanExample(object):
    """Main example class which is run"""

    class State(Enum):
        """State enumeration class"""

        START = auto()

        LOGIN = auto()  # Started on authentication_on_open
        CREATE_BUILDING = auto()
        CREATE_FLOOR_PLAN = auto()
        GET_FLOOR_PLANS = auto()
        SET_FLOOR_PLAN_IMAGE = auto()
        SET_FLOOR_PLAN_IMAGE_THUMBNAIL = auto()
        GET_FLOOR_PLANS_2 = auto()
        UPDATE_FLOOR_PLAN = auto()
        GET_FLOOR_PLAN_IMAGE = auto()
        GET_FLOOR_PLAN_IMAGE_THUMBNAIL = auto()
        DELETE_FLOOR_PLAN = auto()
        DELETE_BUILDING = auto()

        END = auto()

    def __init__(self) -> None:
        """Initialization"""
        self.floor_plan_image_id = None
        self.floor_plan_image_thumbnail_id = None

        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.authentication_thread = None
        self.metadata_thread = None

        self.settings = get_settings()

        self.logger = setup_log("FloorPlanExample", self.settings.log_level)

        self.client = Connections(
            hostname=self.settings.hostname,
            logger=self.logger,
            authentication_on_open=self.authentication_on_open,
            authentication_on_message=self.authentication_on_message,
            authentication_on_error=self.authentication_on_error,
            authentication_on_close=self.authentication_on_close,
            metadata_on_open=self.metadata_on_open,
            metadata_on_message=self.metadata_on_message,
            metadata_on_error=self.metadata_on_error,
            metadata_on_close=self.metadata_on_close,
        )

        self.messages = Messages(self.logger, self.settings.protocol_version)

        script_path = os.path.dirname(os.path.realpath(__file__))

        self.floor_plan_image_file_path = os.path.join(
            script_path, "assets/floor_plan.png"
        )

        self.floor_plan_image_thumbnail_file_path = os.path.join(
            script_path, "assets/floor_plan_thumbnail.png"
        )

        self.temp_floor_plan_image_file_path = (
            self.floor_plan_image_file_path + ".tmp.png"
        )
        self.temp_floor_plan_image_thumbnail_file_path = (
            self.floor_plan_image_thumbnail_file_path + ".tmp.png"
        )

    def send_request(self) -> None:
        """Send request"""
        if self.state == self.State.LOGIN:
            self.authentication_thread.socket.send(
                json.dumps(
                    self.messages.message_login(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state == self.State.CREATE_BUILDING:
            self.metadata_thread.socket.send(
                json.dumps(self.messages.message_create_building("New building"))
            )

        elif self.state == self.State.CREATE_FLOOR_PLAN:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_create_floor_plan(
                        self.messages.new_building_id, "New floor plan"
                    )
                )
            )

        elif self.state.name.startswith(self.State.GET_FLOOR_PLANS.name):
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_get_floor_plans(self.messages.new_building_id)
                )
            )

        elif self.state == self.state.SET_FLOOR_PLAN_IMAGE:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_set_image(
                        FileHelper.read_file_content_as_base64(
                            self.floor_plan_image_file_path
                        )
                    )
                )
            )

        elif self.state == self.state.SET_FLOOR_PLAN_IMAGE_THUMBNAIL:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_set_image(
                        FileHelper.read_file_content_as_base64(
                            self.floor_plan_image_thumbnail_file_path
                        )
                    )
                )
            )

        elif self.state == self.State.UPDATE_FLOOR_PLAN:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_update_floor_plan(
                        self.messages.new_floor_plan_id,
                        image_id=self.floor_plan_image_id,
                        image_thumbnail_id=self.floor_plan_image_thumbnail_id,
                    )
                )
            )

        elif self.state == self.state.GET_FLOOR_PLAN_IMAGE:
            self.metadata_thread.socket.send(
                json.dumps(self.messages.message_get_image(self.floor_plan_image_id))
            )

        elif self.state == self.state.GET_FLOOR_PLAN_IMAGE_THUMBNAIL:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_get_image(self.floor_plan_image_thumbnail_id)
                )
            )

        elif self.state == self.State.DELETE_FLOOR_PLAN:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_delete_floor_plan(
                        self.messages.new_floor_plan_id
                    )
                )
            )

        elif self.state == self.State.DELETE_BUILDING:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_delete_building(self.messages.new_building_id)
                )
            )

    def parse_response(self, message: str) -> bool:
        """Parse response

        Args:
            message (str): received message

        Returns:
            bool: True if response's request succeeded
        """
        if self.state == self.State.LOGIN:
            return self.messages.parse_login(json.loads(message))

        elif self.state == self.State.CREATE_BUILDING:
            return self.messages.parse_create_building(json.loads(message))

        elif self.state == self.State.CREATE_FLOOR_PLAN:
            return self.messages.parse_create_floor_plan(json.loads(message))

        elif self.state.name.startswith(self.State.GET_FLOOR_PLANS.name):
            return self.messages.parse_get_floor_plans(json.loads(message))

        elif self.state == self.State.SET_FLOOR_PLAN_IMAGE:
            parse_result = self.messages.parse_set_image(json.loads(message))

            if parse_result:
                self.floor_plan_image_id = self.messages.image_id

            return parse_result

        elif self.state == self.State.SET_FLOOR_PLAN_IMAGE_THUMBNAIL:
            parse_result = self.messages.parse_set_image(json.loads(message))

            if parse_result:
                self.floor_plan_image_thumbnail_id = self.messages.image_id

            return parse_result

        elif self.state == self.State.GET_FLOOR_PLAN_IMAGE:
            parse_result = self.messages.parse_get_image(json.loads(message))

            if parse_result:
                FileHelper.write_file_content_from_base64(
                    self.temp_floor_plan_image_file_path,
                    self.messages.image_data_base64,
                )

            return parse_result

        elif self.state == self.State.GET_FLOOR_PLAN_IMAGE_THUMBNAIL:
            parse_result = self.messages.parse_get_image(json.loads(message))

            if parse_result:
                FileHelper.write_file_content_from_base64(
                    self.temp_floor_plan_image_thumbnail_file_path,
                    self.messages.image_data_base64,
                )
            return parse_result

        elif self.state == self.State.UPDATE_FLOOR_PLAN:
            return self.messages.parse_update_floor_plan(json.loads(message))

        elif self.state == self.State.DELETE_FLOOR_PLAN:
            return self.messages.parse_delete_floor_plan(json.loads(message))

        elif self.state == self.State.DELETE_BUILDING:
            return self.messages.parse_delete_building(json.loads(message))

    def authentication_on_open(self, _websocket) -> None:
        """Websocket callback when the authentication websocket has been opened

        Args:
            websocket (Websocket): communication socket
        """
        self.logger.info("Authentication socket open")
        self.send_request()

    def authentication_on_message(self, websocket, message: str) -> None:
        """Websocket callback when a new authentication message arrives

        Args:
            websocket (Websocket): communication socket
            message (str): received message
        """
        self.on_message(websocket, message)

    def authentication_on_error(self, websocket, error: str) -> None:
        """Websocket callback when an authentication socket error occurs

        Args:
            websocket (Websocket): communication socket
            error (str): error message
        """
        if websocket.keep_running:
            self.logger.error("Authentication socket error: {0}".format(error))

    def authentication_on_close(self, _websocket) -> None:
        """Websocket callback when the authentication connection closes

        Args:
            _websocket (Websocket): communication socket
        """
        self.logger.info("Authentication socket close")

    def metadata_on_open(self, _websocket) -> None:
        """Websocket callback when the metadata websocket has been opened

        Args:
            websocket (Websocket): communication socket
        """
        self.logger.info("Metadata socket open")

    def metadata_on_message(self, websocket, message: str) -> None:
        """Websocket callback when a new metadata message arrives

        Args:
            websocket (Websocket): communication socket
            message (str): received message
        """
        self.on_message(websocket, message)

    def metadata_on_error(self, websocket, error) -> None:
        """Websocket callback when a metadata socket error occurs

        Args:
            websocket (Websocket): communication socket
            error (str): error message
        """
        if websocket.keep_running:
            self.logger.error("Metadata socket error: {0}".format(error))

    def metadata_on_close(self, _websocket) -> None:
        """Websocket callback when the metadata connection closes

        Args:
            _websocket (Websocket): communication socket
        """
        self.logger.warning("Metadata socket close")

    def on_message(self, _websocket, message: str) -> None:
        """Called when authentication or metadata message is received

        Handles the state machine and closing of the communication threads

        Args:
            websocket (Websocket): communication socket
            message (str): received message
        """
        if not self.parse_response(message):
            self.logger.error("Test run failed. Exiting.")
            self.client.stop_metadata_thread()
            self.client.stop_authentication_thread()
        else:
            self.state = self.State(self.state.value + 1)

            if self.state != self.State.END:
                self.send_request()
            else:
                self.return_code = 0
                self.client.stop_metadata_thread()
                self.client.stop_authentication_thread()

    def run(self) -> int:
        """Run method which starts and waits the communication thread(s)

        Returns:
            int: Process return code
        """
        try:
            self.authentication_thread = self.client.start_authentication_thread()
            self.metadata_thread = self.client.start_metadata_thread()

            self.metadata_thread.join()
            self.authentication_thread.join()
        except:
            pass

        return self.return_code


if __name__ == "__main__":
    exit(FloorPlanExample().run())
