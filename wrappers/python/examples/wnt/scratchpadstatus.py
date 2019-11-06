# pylint: disable=duplicate-code
"""
    Scratchpad status example
    =========================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from utils import get_settings, setup_log
from connections import Connections

import json
import wirepas_messaging.wnt as wnt_proto

from enum import Enum, auto
from wirepas_messaging.wnt.ws_api import (
    RealtimeSituationMessages,
    ScratchpadStatusMessages,
)


class Messages(RealtimeSituationMessages, ScratchpadStatusMessages):
    """Aggregation class for messages"""

    def __init__(self, logger, protocol_version) -> None:
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        RealtimeSituationMessages.__init__(self, logger, protocol_version)
        ScratchpadStatusMessages.__init__(self, logger, protocol_version)


class ComponentsInformationExample(object):
    """Main example class which is run"""

    class State(Enum):
        """State enumeration class"""

        START = auto()

        LOGIN = auto()  # Started on authentication_on_open
        REALTIME_SITUATION_LOGIN = auto()

        WAIT_FOR_STARTUP_SITUATION = auto()
        QUERY_SCRATCHPAD_STATUS = auto()
        WAIT_FOREVER = auto()

        END = auto()

    def __init__(self) -> None:
        """Initialization"""
        self.return_code = -1
        self.state = self.State(self.State.START.value + 1)

        self.authentication_thread = None
        self.metadata_thread = None
        self.realtime_situation_thread = None

        self.total_node_count = 0
        self.loaded_node_count = 0

        self.settings = get_settings()

        self.logger = setup_log("ScratchpadStatusExample", self.settings.log_level)

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
            realtime_situation_on_open=self.realtime_situation_on_open,
            realtime_situation_on_message=self.realtime_situation_on_message,
            realtime_situation_on_error=self.realtime_situation_on_error,
            realtime_situation_on_close=self.realtime_situation_on_close,
        )

        self.messages = Messages(self.logger, self.settings.protocol_version)

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

        elif self.state == self.State.REALTIME_SITUATION_LOGIN:
            self.realtime_situation_thread.socket.send(
                json.dumps(
                    self.messages.message_realtime_situation_login(
                        self.messages.session_id
                    )
                )
            )

        elif self.state == self.State.QUERY_SCRATCHPAD_STATUS:
            self.metadata_thread.socket.send(
                json.dumps(
                    self.messages.message_query_scratchpad_status(777555, 0, False)
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

        elif self.state == self.state.QUERY_SCRATCHPAD_STATUS:
            return self.messages.parse_query_scratchpad_status(json.loads(message))

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

    def realtime_situation_on_open(self, _websocket) -> None:
        """Websocket callback when the realtime situation websocket has been opened

        Args:
            websocket (Websocket): communication socket
        """
        self.logger.info("Realtime situation socket open")

    def realtime_situation_on_message(self, _websocket, message: str) -> None:
        """Websocket callback when a new realtime situation message arrives

        Args:
            websocket (Websocket): communication socket
            message (str): received message
        """
        if self.state == self.State.REALTIME_SITUATION_LOGIN:
            if not self.messages.parse_realtime_situation_login(json.loads(message)):
                self.logger.error("Test run failed. Exiting.")
                self.stop_connection_threads()
            else:
                self.state = self.State(self.state.value + 1)
                self.send_request()

            return

        elif self.state == self.state.WAIT_FOR_STARTUP_SITUATION:
            wnt_message = wnt_proto.Message()
            wnt_message.ParseFromString(message)

            if wnt_message.HasField("rtsituation_metadata"):
                self.total_node_count += wnt_message.rtsituation_metadata.node_count

            if wnt_message.HasField("source_address") and wnt_message.HasField(
                "network_id"
            ):
                # Here it would be good to count distinct node count
                self.loaded_node_count += 1

            if self.loaded_node_count == self.total_node_count:
                # Initial nodes' data loaded
                self.state = self.State(self.state.value + 1)
                self.send_request()

        wnt_message = wnt_proto.Message()
        wnt_message.ParseFromString(message)

        if wnt_message.HasField("scratchpad_status"):
            self.logger.info(
                "scratchpad_status:\nnetwork id: {}\nnode id: {}\n{}".format(
                    wnt_message.network_id,
                    wnt_message.source_address,
                    wnt_message.scratchpad_status,
                )
            )

    def realtime_situation_on_error(self, websocket, error: str) -> None:
        """Websocket callback when realtime situation socket error occurs

        Args:
            websocket (Websocket): communication socket
            error (str): error message
        """
        if websocket.keep_running:
            self.logger.error("Realtime situation socket error: {0}".format(error))

    def realtime_situation_on_close(self, _websocket) -> None:
        """Websocket callback when the realtime situation connection closes

        Args:
            _websocket (Websocket): communication socket
        """
        self.logger.warning("Realtime situation socket close")

    def on_message(self, _websocket, message: str) -> None:
        """Called when authentication or metadata message is received

        Handles the state machine and closing of the communication threads

        Args:
            websocket (Websocket): communication socket
            message (str): received message
        """
        if not self.parse_response(message):
            self.logger.error("Test run failed. Exiting.")
            self.stop_connection_threads()
        elif (
            not self.state == self.State.WAIT_FOR_STARTUP_SITUATION
            and not self.state == self.State.WAIT_FOREVER
        ):
            self.state = self.State(self.state.value + 1)

            if self.state != self.State.END:
                self.send_request()
            else:
                self.return_code = 0
                self.stop_connection_threads()

    def stop_connection_threads(self) -> None:
        """Stop all connection threads"""
        self.client.stop_realtime_situation_thread()
        self.client.stop_metadata_thread()
        self.client.stop_authentication_thread()

    def run(self) -> int:
        """Run method which starts and waits the communication thread(s)

        Returns:
            int: Process return code
        """
        try:
            self.realtime_situation_thread = (
                self.client.start_realtime_situation_thread()
            )
            self.metadata_thread = self.client.start_metadata_thread()
            self.authentication_thread = self.client.start_authentication_thread()

            # Run for 120 seconds
            self.realtime_situation_thread.join(120)
            self.metadata_thread.join(0)
            self.authentication_thread.join(0)

            self.return_code = 0
        except:
            pass

        return self.return_code


if __name__ == "__main__":
    exit(ComponentsInformationExample().run())
