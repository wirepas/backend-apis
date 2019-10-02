"""
    Create user messages for testing
    ================================

    Authentication server create user messages for testing

    .. Copyright:
        Copyright 2019 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""

from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class CreateUser(AuthenticationMessages):
    """The class generates and decodes create user messages for testing"""

    def __init__(self, logger, protocol_version: int) -> None:
        super(CreateUser, self).__init__(logger, protocol_version)

    def message_create_user_wo_version(
        self, username: str, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without version"""
        message = dict(
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        password=password,
                        full_name=full_name,
                        role=role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_session_id(
        self, username: str, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without session id"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        password=password,
                        full_name=full_name,
                        role=role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_type(
        self, username: str, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without type"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            data=dict(
                users=[
                    dict(
                        username=username,
                        password=password,
                        full_name=full_name,
                        role=role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_data(
        self, username: str, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without data"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_username(
        self, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without user name"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[dict(password=password, full_name=full_name, role=role)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_password(
        self, username: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without password"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[dict(username=username, full_name=full_name, role=role)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_full_name(
        self, username: str, password: str, role: int
    ) -> dict:
        """Returns a create user message without full name"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[dict(username=username, password=password, role=role)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_role(
        self, username: str, password: str, full_name: str
    ) -> dict:
        """Returns a create user message without role"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[dict(username=username, password=password, full_name=full_name)],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def message_create_user_wo_originator_token(
        self, username: str, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message without originator token"""
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        password=password,
                        full_name=full_name,
                        role=role,
                    )
                ]
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message
