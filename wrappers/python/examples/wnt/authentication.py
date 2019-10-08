# pylint: disable=duplicate-code
"""
    Authentication example
    ======================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from utils import get_settings, setup_log
from connections import Connections

import json

from enum import Enum, auto
from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class AuthenticationExample(object):
    """Main example class which is run"""

    class State(Enum):
        """State enumeration class"""

        START = auto()

        LOGIN = auto()  # Started on authentication_on_open
        QUERY_USERS = auto()
        CREATE_USER = auto()
        QUERY_USERS_2 = auto()
        UPDATE_USER = auto()
        QUERY_USERS_3 = auto()
        DELETE_USER = auto()
        QUERY_USERS_4 = auto()

        END = auto()

    def __init__(self) -> None:
        """Initialization"""
        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.new_user = dict(
            username="jdoeexample",
            password="secret",
            full_name="John Doe",
            role=AuthenticationMessages.Role.OPERATOR.value,
            updated_full_name="John J. Doe",
            updated_password="secret2",
            updated_role=AuthenticationMessages.Role.ADMIN.value,
        )

        self.settings = get_settings()

        self.logger = setup_log("AuthenticationExample", self.settings.log_level)

        self.client = Connections(
            hostname=self.settings.hostname,
            logger=self.logger,
            authentication_on_open=self.authentication_on_open,
            authentication_on_message=self.authentication_on_message,
            authentication_on_error=self.authentication_on_error,
            authentication_on_close=self.authentication_on_close,
        )

        self.authentication = AuthenticationMessages(
            self.logger, self.settings.protocol_version
        )

    def send_request(self, websocket) -> None:
        """Send request

        Args:
            websocket (Websocket): communication socket
        """
        if self.state.name.startswith(self.State.LOGIN.name):
            websocket.send(
                json.dumps(
                    self.authentication.message_login(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state.name.startswith(self.State.QUERY_USERS.name):
            websocket.send(json.dumps(self.authentication.message_query_users()))

        elif self.state.name.startswith(self.State.CREATE_USER.name):
            websocket.send(
                json.dumps(
                    self.authentication.message_create_user(
                        username=self.new_user["username"],
                        password=self.new_user["password"],
                        full_name=self.new_user["full_name"],
                        role=self.new_user["role"],
                    )
                )
            )

        elif self.state.name.startswith(self.State.UPDATE_USER.name):
            websocket.send(
                json.dumps(
                    self.authentication.message_update_user(
                        username=self.new_user["username"],
                        new_password=self.new_user["updated_password"],
                        new_full_name=self.new_user["updated_full_name"],
                        new_role=self.new_user["updated_role"],
                    )
                )
            )

        elif self.state.name.startswith(self.State.DELETE_USER.name):
            websocket.send(
                json.dumps(
                    self.authentication.message_delete_user(
                        username=self.new_user["username"]
                    )
                )
            )

    def parse_response(self, message: str) -> bool:
        """Parse response

        Args:
            message (str): received message

        Returns:
            bool: True if response's request succeeded
        """
        if self.state.name.startswith(self.State.LOGIN.name):
            if not self.authentication.parse_login(json.loads(message)):
                return False

        elif self.state.name.startswith(self.State.QUERY_USERS.name):
            if not self.authentication.parse_query_users(json.loads(message)):
                return False

        elif self.state.name.startswith(self.State.CREATE_USER.name):
            if not self.authentication.parse_create_user(json.loads(message)):
                return False

        elif self.state.name.startswith(self.State.UPDATE_USER.name):
            if not self.authentication.parse_update_user(json.loads(message)):
                return False

        elif self.state.name.startswith(self.State.DELETE_USER.name):
            if not self.authentication.parse_delete_user(json.loads(message)):
                return False

        return True

    def authentication_on_open(self, websocket) -> None:
        """Websocket callback when the authentication websocket has been opened

        Args:
            websocket (Websocket): communication socket
        """
        self.logger.info("Socket open")
        self.send_request(websocket)

    def authentication_on_message(self, websocket, message: str) -> None:
        """Websocket callback when a new authentication message arrives

        Args:
            websocket (Websocket): communication socket
            message (str): received message
        """
        if not self.parse_response(message):
            self.logger.error("Example run failed. Exiting.")
            self.client.stop_authentication_thread()
        else:
            self.state = self.State(self.state.value + 1)

            if self.state != self.State.END:
                self.send_request(websocket)
            else:
                self.return_code = 0
                self.client.stop_authentication_thread()

    def authentication_on_error(self, websocket, error: str) -> None:
        """Websocket callback when an authentication socket error occurs

        Args:
            _websocket (Websocket): communication socket
            error (str): error message
        """
        if websocket.keep_running:
            self.logger.error("Socket error: {0}".format(error))

    def authentication_on_close(self, _websocket) -> None:
        """Websocket callback when the authentication connection closes

        Args:
            _websocket (Websocket): communication socket
        """
        self.logger.info("Socket close")

    def run(self) -> int:
        """Run method which starts and waits the communication thread(s)

        Returns:
            int: Process return code
        """
        try:
            self.client.start_authentication_thread().join()
        except:
            pass

        return self.return_code


if __name__ == "__main__":
    exit(AuthenticationExample().run())
