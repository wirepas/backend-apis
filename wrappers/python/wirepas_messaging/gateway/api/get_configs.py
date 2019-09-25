"""
    Get configs
    ===========

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .request import Request
from .response import Response

from .config_helper import (
    parse_config_rw,
    parse_config_ro,
    set_config_ro,
    set_config_rw,
)
from .wirepas_exceptions import GatewayAPIParsingException


class GetConfigsRequest(Request):
    """
    GetConfigsRequest: Request to obtain the configs of all sinks from a gateway

    Attributes:
        req_id (int): unique request id
    """

    def __init__(self, req_id=None, **kwargs):
        super(GetConfigsRequest, self).__init__(req_id=req_id, **kwargs)

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse GetConfigsRequest payload")

        d = Request._parse_request_header(message.wirepas.get_configs_req.header)
        return cls(d["req_id"])

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()
        # Fill the request header
        get_config = message.wirepas.get_configs_req
        get_config.header.CopyFrom(self._make_request_header())

        return message.SerializeToString()


class GetConfigsResponse(Response):
    """
    GetConfigsResponse: Response to answer a GetConfigsRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        configs (list): list of dictionnary containing a dict representing an attached sink
    """

    def __init__(self, req_id, gw_id, res, configs, **kwargs):
        super(GetConfigsResponse, self).__init__(req_id, gw_id, res, **kwargs)
        self.configs = configs

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse GetConfigsResponse payload")

        response = message.wirepas.get_configs_resp

        d = Response._parse_response_header(response.header)

        configs = []

        for conf in response.configs:
            config = {}

            config["sink_id"] = conf.sink_id

            parse_config_rw(conf, config)
            parse_config_ro(conf, config)

            configs.append(config)

        return cls(d["req_id"], d["gw_id"], d["res"], configs)

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()

        response = message.wirepas.get_configs_resp
        response.header.CopyFrom(self._make_response_header())

        for config in self.configs:
            conf = response.configs.add()
            conf.sink_id = config["sink_id"]

            set_config_rw(conf, config)
            set_config_ro(conf, config)

        return message.SerializeToString()
