# pylint: disable=duplicate-code
"""
    Components' information
    =======================

    Component information related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class ComponentsInformationMessages(AuthenticationMessages):
    """This class generates and decodes components' information related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(ComponentsInformationMessages, self).__init__(logger, protocol_version)

    def message_query_components_information(self) -> dict:
        """Returns query components' information message"""

        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.QUERY_COMPONENTS_INFORMATION.value,
            data=dict(originator_token=self.originator_token),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_query_components_information(self, message: dict) -> bool:
        """Parses query components' information response

        Args:
            message (dict): the query components' information response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot query components' information")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
