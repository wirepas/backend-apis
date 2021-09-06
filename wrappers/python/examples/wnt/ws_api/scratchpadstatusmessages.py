"""
    Scratchpad status
    =================

    Scratchpad status related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class ScratchpadStatusMessages(AuthenticationMessages):
    """This class generates and decodes scratchpad status related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(ScratchpadStatusMessages, self).__init__(logger, protocol_version)

    def message_get_scratchpad_status(
        self,
        network_id: int,
        resend_interval_s: int,
        is_close: bool,
        is_sink_only: bool,
    ) -> dict:
        """Returns get scratchpad status message

        Args:
            network_id (int): network id
            resend_interval_s (int): how often the get scratchpad should be run
            is_close (bool): set to true to stop repeated gets
            is_sink_only (bool): set to true to get scratchpad status only from sink nodes
        """

        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_SCRATCHPAD_STATUS.value,
            data=dict(
                networks=[
                    dict(
                        id=network_id,
                        resend_interval_s=resend_interval_s,
                        is_close=is_close,
                        is_sink_only=is_sink_only,
                    )
                ]
            ),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_get_scratchpad_status(self, message: dict) -> bool:
        """Parses get scratchpad status response

        Args:
            message (dict): the get scratchpad status response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot query scratchpad status")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
