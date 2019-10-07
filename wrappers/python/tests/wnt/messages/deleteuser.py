"""
    Delete user messages for testing
    ================================

    Authentication server delete user messages for testing

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class DeleteUser(AuthenticationMessages):
    """The class generates and decodes delete user messages for testing"""

    def __init__(self, logger, protocol_version: int) -> None:
        super(DeleteUser, self).__init__(logger, protocol_version)

    def message_delete_user_wo_version(self, username: str) -> dict:
        """Returns a delete user message without version"""
        message = dict(
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_USER.value,
            data=dict(
                users=[dict(username=username)], originator_token=self.originator_token
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_delete_user_wo_session_id(self, username: str) -> dict:
        """Returns a delete user message without session id"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.DELETE_USER.value,
            data=dict(
                users=[dict(username=username)], originator_token=self.originator_token
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_delete_user_wo_type(self, username: str) -> dict:
        """Returns a delete user message without type"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            data=dict(
                users=[dict(username=username)], originator_token=self.originator_token
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_delete_user_wo_data(self) -> dict:
        """Returns a delete user message without data"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_USER.value,
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_delete_user_wo_originator_token(self, username: str) -> dict:
        """Returns a delete user message without orinator token"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.DELETE_USER.value,
            data=dict(users=[dict(username=username)]),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message
