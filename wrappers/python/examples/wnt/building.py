# pylint: disable=duplicate-code
"""
    Buildings example
    =================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from utils import get_settings, setup_log
from connections import Connections

import json

from enum import Enum, auto
from wirepas_messaging.wnt.ws_api import BuildingMessages


class BuildingExample(object):
    """Main example class which is run"""

    class State(Enum):
        """State enumeration class"""

        START = auto()

        LOGIN = auto()  # Started on authentication_on_open
        CREATE_BUILDING = auto()
        GET_BUILDINGS = auto()
        UPDATE_BUILDING = auto()
        GET_BUILDINGS_2 = auto()
        DELETE_BUILDING = auto()

        END = auto()

    def __init__(self) -> None:
        """Initialization"""
        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.authentication_thread = None
        self.metadata_thread = None

        self.settings = get_settings()

        self.logger = setup_log("BuildingExample", self.settings.log_level)

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

        self.messages = BuildingMessages(self.logger, self.settings.protocol_version)

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

        elif self.state.name.startswith(self.State.GET_BUILDINGS.name):
            self.metadata_thread.socket.send(
                json.dumps(self.messages.message_get_buildings())
            )

        elif self.state == self.State.UPDATE_BUILDING:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_update_building(
                        self.messages.new_building_id, "Updated building"
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

        elif self.state.name.startswith(self.State.GET_BUILDINGS.name):
            return self.messages.parse_get_buildings(json.loads(message))

        elif self.state == self.State.UPDATE_BUILDING:
            return self.messages.parse_update_building(json.loads(message))

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

    def metadata_on_error(self, websocket, error: str) -> None:
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
    exit(BuildingExample().run())
