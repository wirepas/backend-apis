"""
    Login test
    ==========

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import wnt
import json

from enum import Enum, auto
from .messages import Login as LoginMessages


class LoginTest:
    """Main test class"""

    class State(Enum):
        """State enum class"""

        START = auto()

        LOGIN_WO_VERSION = auto()
        LOGIN_WO_TYPE = auto()
        LOGIN_WO_USERNAME = auto()
        LOGIN_WO_PASSWORD = auto()
        LOGIN_WRONG_VERSION = auto()
        LOGIN_WRONG_TYPE = auto()
        LOGIN_WRONG_USERNAME = auto()
        LOGIN_WRONG_PASSWORD = auto()
        LOGIN = auto()

        END = auto()

    def __init__(self) -> None:
        """Class initialization"""
        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.settings = wnt.settings()

        self.logger = wnt.utils.setup_log("LoginTest", self.settings.log_level)

        self.client = wnt.Connections(
            hostname=self.settings.hostname,
            logger=self.logger,
            authentication_on_open=self.authentication_on_open,
            authentication_on_message=self.authentication_on_message,
            authentication_on_error=self.authentication_on_error,
            authentication_on_close=self.authentication_on_close,
        )

        self.messages = LoginMessages(self.logger, self.settings.protocol_version)

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

        elif self.state == self.State.LOGIN_WO_VERSION:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_version(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state == self.State.LOGIN_WO_TYPE:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_type(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state == self.State.LOGIN_WO_USERNAME:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_username(self.settings.username)
                )
            )

        elif self.state == self.State.LOGIN_WO_PASSWORD:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_password(self.settings.password)
                )
            )

        elif self.state == self.State.LOGIN_WRONG_VERSION:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_version(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state == self.State.LOGIN_WRONG_TYPE:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_type(
                        self.settings.username, self.settings.password
                    )
                )
            )

        elif self.state == self.State.LOGIN_WRONG_USERNAME:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_username(self.settings.username)
                )
            )

        elif self.state == self.State.LOGIN_WRONG_PASSWORD:
            websocket.send(
                json.dumps(
                    self.messages.message_login_wo_password(self.settings.password)
                )
            )

    def parse_response(self, message) -> bool:
        """Parse response"""
        if self.state == self.State.LOGIN:
            return self.messages.parse_login(json.loads(message))

        if self.state.name.startswith("LOGIN_WO_") or self.state.name.startswith(
            "LOGIN_WRONG_"
        ):
            return not self.messages.parse_login(json.loads(message))

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
    exit_code = LoginTest().run()
    if exit_code != 0:
        raise ValueError("Incorrect exit code. Exit code: {}".format(exit_code))


if __name__ == "__main__":
    test_main()
