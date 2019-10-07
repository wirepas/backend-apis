"""
    Update user messages for testing
    ================================

    Authentication server update user messages for testing

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class UpdateUser(AuthenticationMessages):
    """The class generates and decodes create user messages for testing"""

    def __init__(self, logger, protocol_version: int) -> None:
        super(UpdateUser, self).__init__(logger, protocol_version)

    def message_update_user_wo_version(
        self,
        username: str,
        updated_password: str,
        updated_full_name: str,
        updated_role: int,
    ) -> dict:
        """Returns an update user message without version"""
        message = dict(
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        full_name=updated_full_name,
                        password=updated_password,
                        role=updated_role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_wo_session_id(
        self,
        username: str,
        updated_password: str,
        updated_full_name: str,
        updated_role: int,
    ) -> dict:
        """Returns an update user message without session id"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        full_name=updated_full_name,
                        password=updated_password,
                        role=updated_role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_wo_type(
        self,
        username: str,
        updated_password: str,
        updated_full_name: str,
        updated_role: int,
    ) -> dict:
        """Returns an update user message without type"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            data=dict(
                users=[
                    dict(
                        username=username,
                        full_name=updated_full_name,
                        password=updated_password,
                        role=updated_role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_wo_data(self) -> dict:
        """Returns an update user message without data"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_wo_originator_token(
        self,
        username: str,
        updated_password: str,
        updated_full_name: str,
        updated_role: int,
    ) -> dict:
        """Returns an update user message without originator token"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        full_name=updated_full_name,
                        password=updated_password,
                        role=updated_role,
                    )
                ]
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_wo_username(
        self, updated_password: str, updated_full_name: str, updated_role: int
    ) -> dict:
        """Returns an update user message without user name"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[
                    dict(
                        full_name=updated_full_name,
                        password=updated_password,
                        role=updated_role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_only_password(
        self, username: str, updated_password: str
    ) -> dict:
        """Returns an update user message with user name and password"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[dict(username=username, password=updated_password)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_only_full_name(
        self, username: str, updated_full_name: str
    ) -> dict:
        """Returns an update user message with user name and password"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[dict(username=username, full_name=updated_full_name)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_update_user_only_role(self, username: str, updated_role: int) -> dict:
        """Returns an update user message with user name and role"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[dict(username=username, role=updated_role)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message
