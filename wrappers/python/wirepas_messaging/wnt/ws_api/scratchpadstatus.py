"""
    Scratchpad status
    =================

    Scratchpad status related metadata connection messages

    .. Copyright:
        Copyright 2019 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
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

    def message_query_scratchpad_status(self,
                                        network_id: int,
                                        rerun_interval_s: int,
                                        is_close: bool) -> dict:
        """Returns query scratchpad status message"""

        message = dict(version=self.protocol_version,
                       session_id=self.session_id,
                       type=AuthenticationMessages.MessageTypes.QUERY_SCRATCHPAD_STATUS.value,
                       data=dict(
                           networks=[
                               dict(id=network_id,
                                    rerun_interval_s=rerun_interval_s,
                                    is_close=is_close)
                           ]
                       ))

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_query_scratchpad_status(self, message: dict) -> bool:
        """Parses query scratchpad status response

        Args:
            message (dict): the query scratchpad status response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error('Cannot query scratchpad status')
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
