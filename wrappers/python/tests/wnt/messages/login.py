"""
    Login messages for testing
    ==========================

    Authentication server login messages for testing

    .. Copyright:
        Copyright 2019 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""

from wirepas_messaging.wnt.ws_api import AuthenticationMessages


class Login(AuthenticationMessages):
    """The class generates and decodes login messages for testing"""

    def __init__(self, logger, protocol_version: int) -> None:
        super(Login, self).__init__(logger, protocol_version)

    def message_login_wo_version(self, username: str, password: str) -> dict:
        """Returns a login request message without version"""
        message = dict(
            type=AuthenticationMessages.MessageTypes.LOGIN.value,
            data=dict(username=username, password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wo_type(self, username: str, password: str) -> dict:
        """Returns a login request message without type"""
        message = dict(
            version=self.protocol_version,
            data=dict(username=username, password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wo_username(self, password: str) -> dict:
        """Returns a login request message without user name"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.LOGIN.value,
            data=dict(password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wo_password(self, username: str) -> dict:
        """Returns a login request message without password"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.LOGIN.value,
            data=dict(username=username),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wrong_version(self, username: str, password: str) -> dict:
        """Returns a login request message with wrong version"""
        message = dict(
            type=AuthenticationMessages.MessageTypes.LOGIN.value,
            version=34,
            data=dict(username=username, password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wrong_type(self, username: str, password: str) -> dict:
        """Returns a login request message with wrong type"""
        message = dict(
            version=self.protocol_version,
            type=123,
            data=dict(username=username, password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wrong_username(self, password: str) -> dict:
        """Returns a login request message with wrong user name"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.LOGIN.value,
            data=dict(username="incorrect", password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def message_login_wrong_password(self, username: str) -> dict:
        """Returns a login request message with wrong password"""
        message = dict(
            version=self.protocol_version,
            type=AuthenticationMessages.MessageTypes.LOGIN.value,
            data=dict(username=username, password="something"),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message
