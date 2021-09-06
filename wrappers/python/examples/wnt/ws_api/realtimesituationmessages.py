# pylint: disable=duplicate-code
"""
    Realtime situation
    ==================

    Realtime situation server messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class RealtimeSituationMessages(AuthenticationMessages):
    """This class generates and decodes realtime situation connection messages"""

    def __init__(self, logger, protocol_version) -> None:
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of realtime situation connection
        """
        super(RealtimeSituationMessages, self).__init__(logger, protocol_version)

    def message_realtime_situation_login(self, session_id: str) -> dict:
        """Returns a login request message

        Args:
            session_id (str): session id received from authentication server

        Returns:
            dict: Message dictionary
        """
        message = dict(version=self.protocol_version, session_id=session_id)

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_realtime_situation_login(self, message: dict) -> bool:
        """Parse the login response

        Args:
            message (dict): the login response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot login")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
