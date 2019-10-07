# pylint: disable=duplicate-code
"""
    Authentication
    ==============

    Authentication server messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import enum
from .messagesbase import MessagesBase


class AuthenticationMessages(MessagesBase):
    """This class generates and decodes authentication connection messages"""

    class Role(enum.Enum):
        """User role enum class"""

        ADMIN = 1
        OPERATOR = 2

    def __init__(self, logger, protocol_version) -> None:
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(AuthenticationMessages, self).__init__(logger, protocol_version)

        self.user_role = None
        self.session_id = None
        self.originator_token = "sometoken"

    def message_login(self, username: str, password: str) -> dict:
        """Returns a login request message

        Args:
            username (str): username
            password (str): password

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            type=MessagesBase.MessageTypes.LOGIN.value,
            data=dict(username=username, password=password),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_login(self, message: dict) -> bool:
        """Retrieves the session id from the login request

        Args:
            message (dict): the login message

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

        data = message["data"]

        self.user_role = data["role"]
        self.session_id = data["session_id"]

        return data

    def message_logout(self) -> dict:
        """
        Returns a logout request message

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=MessagesBase.MessageTypes.LOGOUT.value,
            data=dict(),
        )

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_logout(self, message: dict) -> bool:
        """Prints logout response message

        Args:
            message (dict): the logout message

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot logout")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_query_users(self) -> dict:
        """
        Returns a query users message

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=MessagesBase.MessageTypes.GET_USERS.value,
            data=dict(),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def parse_query_users(self, message: dict) -> bool:
        """Prints query users response message

        Args:
            message (dict): the query users response message

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot query users")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_create_user(
        self, username: str, password: str, full_name: str, role: int
    ) -> dict:
        """Returns a create user message

        Args:
            username (str): username
            password (str): password
            full_name (str): full name
            role (str): role

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=MessagesBase.MessageTypes.CREATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        full_name=full_name,
                        password=password,
                        role=role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def parse_create_user(self, message: dict) -> bool:
        """Prints create user response message

        Args:
            message (dict): the create user response message

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot create user")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_update_user(
        self, username: str, new_password: str, new_full_name: str, new_role: int
    ) -> dict:
        """Returns an update user message

        Args:
            username (str): user's username
            new_password (str): new password
            new_full_name (str): new full name
            new_role (str): new role

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=MessagesBase.MessageTypes.UPDATE_USER.value,
            data=dict(
                users=[
                    dict(
                        username=username,
                        full_name=new_full_name,
                        password=new_password,
                        role=new_role,
                    )
                ],
                originator_token=self.originator_token,
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def parse_update_user(self, message: dict) -> bool:
        """Prints update user response message

        Args:
            message (dict): the update user response message

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot update user")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True

    def message_delete_user(self, username: str) -> dict:
        """Returns a delete user message

        Args:
            username (str): user's username

        Returns:
            dict: Message dictionary
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=MessagesBase.MessageTypes.DELETE_USER.value,
            data=dict(
                users=[dict(username=username)], originator_token=self.originator_token
            ),
        )

        self.logger.info(self.json_dump_pretty(message))

        return message

    def parse_delete_user(self, message: dict) -> bool:
        """Prints delete user response message

        Args:
            message (dict): the delete user response message

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot delete user")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
