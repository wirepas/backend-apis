# pylint: disable=duplicate-code
"""
    Application configuration
    =========================

    Application configuration related metadata connection messages

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
from .authenticationmessages import AuthenticationMessages


class ApplicationConfigurationMessages(AuthenticationMessages):
    """This class generates and decodes application configuration related metadata connection messages"""

    def __init__(self, logger, protocol_version):
        """Initialization

        Args:
            logger (Logger): logger
            protocol_version (int): protocol version of authentication and metadata connection
        """
        super(ApplicationConfigurationMessages, self).__init__(logger, protocol_version)

    def message_set_app_config(
        self,
        network_id: int,
        diagnostics_interval_in_s: int,
        application_data_in_hex: str,
        is_override_on: bool,
        sink_ids: [],
    ) -> dict:
        """Returns application configuration setting message

        For diagnostics interval values please see WP-RM-100 – Wirepas Mesh DualMCU API Reference Manual

        Args:
            network_id (int): network id
            diagnostics_interval_in_s (int): diagnostics interval in seconds
            application_data_in_hex (str): application data as hexadecimal string
            is_override_on (bool): should WNT override the appconfig
                                   if it notices that it has been changed from
                                   outside of WNT
            sink_ids (list of int): sink ids for which the appconfig is set
        """
        message = dict(
            version=self.protocol_version,
            session_id=self.session_id,
            type=AuthenticationMessages.MessageTypes.SET_NETWORK_DATA.value,
            data=dict(
                networks=[
                    dict(
                        id=network_id,
                        diagnostics_interval=diagnostics_interval_in_s,
                        application_data=application_data_in_hex,
                        is_override_on=is_override_on,
                    )
                ]
            ),
            originator_token=self.originator_token,
        )

        if sink_ids is not None:
            message["data"]["networks"][0]["sink_node_ids"] = sink_ids

        self.logger.info(self.json_dump_pretty(message))
        return message

    def parse_set_app_config(self, message: dict) -> bool:
        """Parses application configuration setting response

        Args:
            message (dict): the create area response

        Returns:
            bool: True if message validation succeeded, else False
        """
        try:
            self.validate(message)
            self.logger.info(self.json_dump_pretty(message))
        except ValueError:
            self.logger.error("Cannot set application config")
            self.logger.error(self.json_dump_pretty(message))
            return False

        return True
