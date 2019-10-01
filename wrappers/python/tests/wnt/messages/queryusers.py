"""
    Query users messages for testing
    ================================

    Authentication server query users messages for testing

    .. Copyright:
        Copyright 2019 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""

from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class QueryUsers(AuthenticationMessages):
    """The class generates and decodes query users messages for testing"""

    def __init__(self, logger, protocol_version: int) -> None:
        super(QueryUsers, self).__init__(logger, protocol_version)

    def message_query_users_wo_version(self) -> dict:
        """Returns a query users message without version"""
        message = dict(
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_USERS.value,
            data=dict(),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_query_users_wo_session_id(self) -> dict:
        """Returns a query users message without session id"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.GET_USERS.value,
            data=dict(),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_query_users_wo_type(self) -> dict:
        """Returns a query users message without type"""
        message = dict(
            version=self.protocol_version, session_id=self.session_id, data=dict()
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_query_users_wo_data(self) -> dict:
        """Returns a query users message without data"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.GET_USERS.value,
        )

        self.logger.info(self.json_dump_pretty(message))

        return message
