"""
    Query users test
    ================

    .. Copyright:
        Copyright 2019 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.

"""
import wnt
import json

from enum import Enum, auto
from .messages import QueryUsers as QueryUsersMessages


class QueryUsersTest:
    """Main test class"""

    class State(Enum):
        """State enum class"""

        START = auto()

        LOGIN_AS_OPERATOR = auto()
        QUERY_USERS_AS_OPERATOR = auto()
        LOGOUT = auto()

        QUERY_USERS_WO_LOGIN = auto()

        LOGIN = auto()
        QUERY_USERS_WO_VERSION = auto()
        QUERY_USERS_WO_SESSION_ID = auto()
        QUERY_USERS_WO_TYPE = auto()
        QUERY_USERS_WO_DATA = auto()
        QUERY_USERS = auto()

        END = auto()

    def __init__(self) -> None:
        """Class initialization"""
        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.settings = wnt.settings()

        self.logger = wnt.utils.setup_log("QueryUsersTest", self.settings.log_level)

        self.client = wnt.Connections(
            hostname=self.settings.hostname,
            logger=self.logger,
            authentication_on_open=self.authentication_on_open,
            authentication_on_message=self.authentication_on_message,
            authentication_on_error=self.authentication_on_error,
            authentication_on_close=self.authentication_on_close,
        )

        self.messages = QueryUsersMessages(self.logger, self.settings.protocol_version)

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

        elif (
            self.state == self.State.QUERY_USERS
            or self.state == self.State.QUERY_USERS_WO_LOGIN
            or self.state == self.State.QUERY_USERS_AS_OPERATOR
        ):
            websocket.send(json.dumps(self.messages.message_query_users()))

        elif self.state == self.State.QUERY_USERS_WO_VERSION:
            websocket.send(json.dumps(self.messages.message_query_users_wo_version()))

        elif self.state == self.State.QUERY_USERS_WO_SESSION_ID:
            websocket.send(
                json.dumps(self.messages.message_query_users_wo_session_id())
            )

        elif self.state == self.State.QUERY_USERS_WO_TYPE:
            websocket.send(json.dumps(self.messages.message_query_users_wo_type()))

        elif self.state == self.State.QUERY_USERS_WO_DATA:
            websocket.send(json.dumps(self.messages.message_query_users_wo_data()))

    def parse_response(self, message) -> bool:
        """Parse response"""
        if self.state == self.State.LOGIN or self.state == self.State.LOGIN_AS_OPERATOR:
            return self.messages.parse_login(json.loads(message))

        elif self.state == self.State.LOGOUT:
            return self.messages.parse_logout(json.loads(message))

        if self.state == self.State.QUERY_USERS:
            return self.messages.parse_query_users(json.loads(message))

        if (
            self.state.name.startswith("QUERY_USERS_WO_")
            or self.state == self.State.QUERY_USERS_AS_OPERATOR
        ):
            return not self.messages.parse_query_users(json.loads(message))

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
    exit_code = QueryUsersTest().run()
    if exit_code != 0:
        raise ValueError("Incorrect exit code. Exit code: {}".format(exit_code))


if __name__ == "__main__":
    test_main()
