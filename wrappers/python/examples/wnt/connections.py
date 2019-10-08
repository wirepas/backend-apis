"""
    Connections
    ===========

    WNT backend connections

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import ssl
import logging
import websocket
import threading


class Connections(object):
    """
    Connections

    This class handles websocket connections to WNT backend
    """

    PROTOCOL = "wss"
    AUTHENTICATION_PORT = 8813
    METADATA_PORT = 8812
    REALTIME_SITUATION_PORT = 8811

    def __init__(
        self,
        hostname: str,
        authentication_port: int = None,
        metadata_port: int = None,
        realtime_situation_port: int = None,
        logger=None,
        authentication_on_open=None,
        authentication_on_message=None,
        authentication_on_error=None,
        authentication_on_close=None,
        metadata_on_open=None,
        metadata_on_message=None,
        metadata_on_error=None,
        metadata_on_close=None,
        realtime_situation_on_open=None,
        realtime_situation_on_message=None,
        realtime_situation_on_error=None,
        realtime_situation_on_close=None,
    ):

        super(Connections, self).__init__()

        self.logger = logger or logging.getLogger(__name__)

        self.authentication_on_open = authentication_on_open
        self.authentication_on_message = authentication_on_message
        self.authentication_on_error = authentication_on_error
        self.authentication_on_close = authentication_on_close

        self.metadata_on_open = metadata_on_open
        self.metadata_on_message = metadata_on_message
        self.metadata_on_error = metadata_on_error
        self.metadata_on_close = metadata_on_close

        self.realtime_situation_on_open = realtime_situation_on_open
        self.realtime_situation_on_message = realtime_situation_on_message
        self.realtime_situation_on_error = realtime_situation_on_error
        self.realtime_situation_on_close = realtime_situation_on_close

        self.endpoints = dict(
            auth="{0}://{1}:{2}".format(
                self.PROTOCOL, hostname, authentication_port or self.AUTHENTICATION_PORT
            ),
            meta="{0}://{1}:{2}".format(
                self.PROTOCOL, hostname, metadata_port or self.METADATA_PORT
            ),
            rtsituation="{0}://{1}:{2}".format(
                self.PROTOCOL,
                hostname,
                realtime_situation_port or self.REALTIME_SITUATION_PORT,
            ),
        )

        self._auth_socket = self._create_auth_socket()
        self._metadata_socket = self._create_meta_socket()
        self._realtime_situation_socket = self._create_realtime_situation_socket()

    # socket establishment
    def _create_auth_socket(self, with_trace=True) -> websocket.WebSocketApp:
        websocket.enableTrace(with_trace)
        ws = websocket.WebSocketApp(
            self.endpoints["auth"],
            on_open=self.authentication_on_open,
            on_message=self.authentication_on_message,
            on_error=self.authentication_on_error,
            on_close=self.authentication_on_close,
        )

        return ws

    def _create_meta_socket(self, with_trace=True) -> websocket.WebSocketApp:
        websocket.enableTrace(with_trace)
        ws = websocket.WebSocketApp(
            self.endpoints["meta"],
            on_open=self.metadata_on_open,
            on_message=self.metadata_on_message,
            on_error=self.metadata_on_error,
            on_close=self.metadata_on_close,
        )

        return ws

    def _create_realtime_situation_socket(
        self, with_trace=True
    ) -> websocket.WebSocketApp:
        websocket.enableTrace(with_trace)
        ws = websocket.WebSocketApp(
            self.endpoints["rtsituation"],
            on_open=self.realtime_situation_on_open,
            on_message=self.realtime_situation_on_message,
            on_error=self.realtime_situation_on_error,
            on_close=self.realtime_situation_on_close,
        )

        return ws

    # thread handling
    def start_authentication_thread(self):
        """Starts the authentication connection"""
        authentication_thread = threading.Thread(
            target=self.run, args=(self._auth_socket,)
        )
        authentication_thread.socket = self._auth_socket
        authentication_thread.daemon = True
        authentication_thread.start()
        return authentication_thread

    def stop_authentication_thread(self):
        self._auth_socket.keep_running = False

        if self._auth_socket.sock.connected:
            self._auth_socket.close()

    def start_metadata_thread(self):
        """Starts the metadata connection"""
        metadata_thread = threading.Thread(
            target=self.run, args=(self._metadata_socket,)
        )
        metadata_thread.socket = self._metadata_socket
        metadata_thread.daemon = True
        metadata_thread.start()
        return metadata_thread

    def stop_metadata_thread(self):
        self._metadata_socket.keep_running = False

        if self._metadata_socket.sock.connected:
            self._metadata_socket.close()

    def start_realtime_situation_thread(self):
        """Starts the realtime situation connection"""
        realtime_situation_thread = threading.Thread(
            target=self.run, args=(self._realtime_situation_socket,)
        )
        realtime_situation_thread.socket = self._realtime_situation_socket
        realtime_situation_thread.daemon = True
        realtime_situation_thread.start()
        return realtime_situation_thread

    def stop_realtime_situation_thread(self):
        self._realtime_situation_socket.keep_running = False

        if self._realtime_situation_socket.sock.connected:
            self._realtime_situation_socket.close()

    @staticmethod
    def run(ws: websocket.WebSocketApp):
        """Starts the websocket loop"""
        ws.run_forever(
            sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False},
            ping_interval=10,
        )
