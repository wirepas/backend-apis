"""
    Generic message
    ========

    .. Copyright:
        Copyright 2020 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .wirepas_exceptions import GatewayAPIParsingException


class GenericMessage(object):
    """
    Generic message

    Base class for all Events, Requests, Response

    """

    @classmethod
    def from_generic_message(cls, message):
        """ Implement how to parse message """
        raise NotImplementedError()

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse payload for %s" % cls.__name__
            )

        return cls.from_generic_message(message)

    @property
    def generic_message(self):
        """ Implement how to generate generic message"""
        raise NotImplementedError()

    @property
    def payload(self):
        return self.generic_message.SerializeToString()

    def __str__(self):
        return str(self.__dict__)
