"""
    Update user test
    ================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import wnt
import json

from enum import Enum, auto
from .messages import UpdateUser as UpdateUserMessages


class UpdateUserTest:
    """Main test class"""

    class State(Enum):
        """State enum class"""

        START = auto()

        LOGIN_AS_OPERATOR = auto()
        UPDATE_USER_AS_OPERATOR = auto()
        LOGOUT = auto()

        UPDATE_USER_WO_LOGIN = auto()

        LOGIN = auto()
        DELETE_USER = auto()
        CREATE_USER = auto()
        UPDATE_USER_WO_VERSION = auto()
        UPDATE_USER_WO_SESSION_ID = auto()
        UPDATE_USER_WO_TYPE = auto()
        UPDATE_USER_WO_DATA = auto()
        UPDATE_USER_WO_ORIGINATOR_TOKEN = auto()
        UPDATE_USER_WO_USERNAME = auto()
        UPDATE_USER_ONLY_PASSWORD = auto()
        UPDATE_USER_ONLY_FULL_NAME = auto()
        UPDATE_USER_ONLY_ROLE = auto()
        UPDATE_USER = auto()
        DELETE_USER_2 = auto()

        END = auto()

    def __init__(self) -> None:
        """Class initialization"""
        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.user = dict(
            username="jdoetest",
            password="secret",
            full_name="John Doe",
            role=UpdateUserMessages.Role.OPERATOR.value,
        )

        self.settings = wnt.settings()

        self.logger = wnt.utils.setup_log("UpdateUserTest", self.settings.log_level)

        self.client = wnt.Connections(
            hostname=self.settings.hostname,
            logger=self.logger,
            authentication_on_open=self.authentication_on_open,
            authentication_on_message=self.authentication_on_message,
            authentication_on_error=self.authentication_on_error,
            authentication_on_close=self.authentication_on_close,
        )

        self.messages = UpdateUserMessages(self.logger, self.settings.protocol_version)

    def send_request(self, websocket) -> None:
        """Send request"""
        if self.state == self.State.LOGIN:
            websocket.send(
                json.dumps(
                    self.messages.message_login(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state == self.State.LOGIN_AS_OPERATOR:
            websocket.send(
                json.dumps(
                    self.messages.message_login(
                        self.settings.operator_username, self.settings.operator_password
                    )
                )
            )

        elif self.state == self.State.LOGOUT:
            websocket.send(json.dumps(self.messages.message_logout()))

        elif self.state == self.State.CREATE_USER:
            websocket.send(
                json.dumps(
                    self.messages.message_create_user(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state.name.startswith("DELETE_USER"):
            websocket.send(
                json.dumps(self.messages.message_delete_user(self.user["username"]))
            )

        elif (
            self.state == self.State.UPDATE_USER
            or self.state == self.State.UPDATE_USER_AS_OPERATOR
        ):
            websocket.send(
                json.dumps(
                    self.messages.message_update_user(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_WO_LOGIN:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_wo_version(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_WO_VERSION:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_wo_version(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_WO_SESSION_ID:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_wo_session_id(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_WO_TYPE:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_wo_type(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_WO_DATA:
            websocket.send(json.dumps(self.messages.message_update_user_wo_data()))

        elif self.state == self.State.UPDATE_USER_WO_ORIGINATOR_TOKEN:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_wo_originator_token(
                        self.user["username"],
                        self.user["password"],
                        self.user["full_name"],
                        self.user["role"],
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_WO_USERNAME:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_wo_username(
                        self.user["password"], self.user["full_name"], self.user["role"]
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_ONLY_PASSWORD:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_only_password(
                        self.user["username"], self.user["password"]
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_ONLY_FULL_NAME:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_only_full_name(
                        self.user["username"], self.user["full_name"]
                    )
                )
            )

        elif self.state == self.State.UPDATE_USER_ONLY_ROLE:
            websocket.send(
                json.dumps(
                    self.messages.message_update_user_only_role(
                        self.user["username"], self.user["role"]
                    )
                )
            )

    def parse_response(self, message) -> bool:
        """Parse response"""
        if self.state == self.State.LOGIN or self.state == self.State.LOGIN_AS_OPERATOR:
            return self.messages.parse_login(json.loads(message))

        elif self.state == self.State.LOGOUT:
            return self.messages.parse_logout(json.loads(message))

        elif self.state == self.State.CREATE_USER:
            return self.messages.parse_create_user(json.loads(message))

        elif self.state == self.State.DELETE_USER:
            return True

        elif self.state == self.State.DELETE_USER_2:
            return self.messages.parse_delete_user(json.loads(message))

        elif self.state == self.State.UPDATE_USER:
            return self.messages.parse_update_user(json.loads(message))

        elif (
            self.state.name.startswith("UPDATE_USER_WO_")
            or self.state.name.startswith("UPDATE_USER_ONLY_")
            or self.state == self.State.UPDATE_USER_AS_OPERATOR
        ):
            return not self.messages.parse_update_user(json.loads(message))

    def authentication_on_open(self, websocket) -> None:
        """Websocket callback when the websocket has been opened"""
        self.logger.info("Socket open")
        self.send_request(websocket)

    def authentication_on_message(self, websocket, message) -> None:
        """Websocket callback when a new message arrives"""
        if not self.parse_response(message):
            self.logger.error("Test run failed. Exiting.")
            self.client.stop_authentication_thread()
        else:
            self.state = self.State(self.state.value + 1)

            if self.state != self.State.END:
                self.send_request(websocket)
            else:
                self.return_code = 0
                self.client.stop_authentication_thread()

    def authentication_on_error(self, _websocket, error) -> None:
        """Websocket callback when an error occurs"""
        self.logger.error("Socket error: {0}".format(error))

    def authentication_on_close(self, _websocket) -> None:
        """Websocket callback when the connection closes"""
        self.logger.info("Socket close")

    def run(self) -> int:
        """Method for running the test"""
        try:
            self.client.start_authentication_thread().join()
        except:
            pass

        return self.return_code


def test_main():
    """Testing main entry point"""
    exit_code = UpdateUserTest().run()
    if exit_code != 0:
        raise ValueError("Incorrect exit code. Exit code: {}".format(exit_code))


if __name__ == "__main__":
    test_main()
