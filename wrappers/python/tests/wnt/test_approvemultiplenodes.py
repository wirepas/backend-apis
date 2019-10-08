"""
    Approve multiple nodes test
    ===========================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import wnt
import json

from enum import Enum, auto
from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class ApproveMultipleNodesTest:
    """Main test class"""

    class State(Enum):
        """State enum class"""

        START = auto()

        LOGIN = auto()
        APPROVE_MULTIPLE_NODES = auto()

        END = auto()

    def __init__(self) -> None:
        """Class initialization"""
        self.return_code = -1

        self.state = self.State(self.State.START.value + 1)

        self.authentication_thread = None
        self.metadata_thread = None

        self.settings = wnt.settings()

        self.logger = wnt.utils.setup_log(
            "ApproveMultipleNodesTest", self.settings.log_level
        )

        self.client = wnt.Connections(
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

        self.messages = AuthenticationMessages(
            self.logger, self.settings.protocol_version
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

        elif self.state == self.State.APPROVE_MULTIPLE_NODES:
            message = dict(
                session_id=self.messages.session_id,
                version=self.messages.protocol_version,
                type=AuthenticationMessages.MessageTypes.SET_NODE_METADATA.value,
                data=dict(
                    nodes=[
                        dict(
                            id=1,
                            network_id=12345,
                            name="",
                            description="",
                            rssi_offset=0,
                            latitude=10.00001,
                            longitude=10.00002,
                            altitude=0,
                            pixel_location_x=-1,
                            pixel_location_y=-1,
                            is_approved=True,
                            is_virtual=False,
                        ),
                        dict(
                            id=2,
                            network_id=12345,
                            name="",
                            description="",
                            rssi_offset=0,
                            latitude=10.00011,
                            longitude=10.00012,
                            altitude=0,
                            pixel_location_x=-1,
                            pixel_location_y=-1,
                            is_approved=True,
                            is_virtual=False,
                        ),
                    ],
                    originator_token=self.messages.originator_token,
                ),
            )

            self.logger.info(self.messages.json_dump_pretty(message))

            self.metadata_thread.socket.send(json.dumps(message))

    def parse_response(self, message) -> bool:
        """Parse response"""
        if self.state == self.State.LOGIN:
            return self.messages.parse_login(json.loads(message))

        elif self.state == self.State.APPROVE_MULTIPLE_NODES:
            message_dict = json.loads(message)
            self.logger.info(self.messages.json_dump_pretty(message_dict))
            try:
                return (
                    message_dict["version"] == self.messages.protocol_version
                    and message_dict["type"]
                    == AuthenticationMessages.MessageTypes.SET_NODE_METADATA.value
                    and message_dict["result"] == 1
                )
            except:
                return False

    # Authentication callbacks
    def authentication_on_open(self, websocket) -> None:
        """Websocket callback when the websocket has been opened"""
        self.logger.info("Authentication socket open")
        self.send_request()

    def authentication_on_message(self, websocket, message) -> None:
        """Websocket callback when a new message arrives"""
        self.on_message(websocket, message)

    def authentication_on_error(self, websocket, error) -> None:
        """Websocket callback when an error occurs"""
        if websocket.keep_running:
            self.logger.error("Authentication socket error: {0}".format(error))

    def authentication_on_close(self, _websocket) -> None:
        """Websocket callback when the connection closes"""
        self.logger.info("Authentication socket close")

    # Metadata callbacks
    def metadata_on_open(self, _websocket) -> None:
        """Websocket callback when the metadata ws has been opened"""
        self.logger.info("Metadata socket open")

    def metadata_on_message(self, websocket, message: str) -> None:
        """Websocket callback when a new message arrives in the metadata ws"""
        self.on_message(websocket, message)

    def metadata_on_error(self, websocket, error) -> None:
        """Websocket callback when an error occurs with the metadata ws"""
        if websocket.keep_running:
            self.logger.error("Metadata socket error: {0}".format(error))

    def metadata_on_close(self, _websocket) -> None:
        """Websocket callback when the metadata ws closes"""
        self.logger.warning("Metadata socket close")

    def on_message(self, _websocket, message):
        """Common on message callback"""
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
        """Method for running the test"""
        try:
            self.authentication_thread = self.client.start_authentication_thread()
            self.metadata_thread = self.client.start_metadata_thread()

            self.metadata_thread.join()
            self.authentication_thread.join()
        except:
            pass

        return self.return_code


def test_main():
    """Testing main entry point"""
    exit_code = ApproveMultipleNodesTest().run()
    if exit_code != 0:
        raise ValueError("Incorrect exit code. Exit code: {}".format(exit_code))


if __name__ == "__main__":
    test_main()
