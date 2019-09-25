"""
    Set config
    ==========

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .request import Request
from .response import Response

from .config_helper import (
    parse_config_rw,
    parse_config_keys,
    set_config_rw,
    set_config_keys,
    parse_config_ro,
    set_config_ro,
)
from .wirepas_exceptions import GatewayAPIParsingException


class SetConfigRequest(Request):
    """
    SetConfigRequest: request to set config on a given sink

    Attributes:
        sink_id (str): id of the sink (dependant on gateway)
        new_config (dict): dictionnary containing the new config.
                Dict keys are:
                    node_role (int): Wirepas role
                    node_address (int)
                    network_address (int)
                    network_channel (int)
                    app_config_diag (int)
                    app_config_seq (int)
                    app_config_data (bytearray)
                    channel_map (int): discarded if not supported by sink
                    cipher_key (bytearray)
                    authentication_key (bytearray)
                    started (bool)

                Note: app_config_data/app_config_seq/app_config_data must all be defined to change one of them
                      only relevant keys for new config has to be defined
        req_id (int): unique request id
    """

    def __init__(self, sink_id, new_config, req_id=None, **kwargs):
        super(SetConfigRequest, self).__init__(req_id=req_id, **kwargs)
        self.sink_id = sink_id
        self.new_config = new_config

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse SetConfigRequest payload")

        req = message.wirepas.set_config_req

        d = Request._parse_request_header(req.header)

        if (d["sink_id"] is not None) and (d["sink_id"] != req.config.sink_id):
            print("Warning: Mismatch in sink id for set_config_request")

        new_config = {}
        new_config["sink_id"] = req.config.sink_id
        parse_config_rw(req.config, new_config)
        parse_config_keys(req.config, new_config)

        return cls(req.config.sink_id, new_config, d["req_id"])

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()
        # Fill the request header
        set_config = message.wirepas.set_config_req
        set_config.header.CopyFrom(self._make_request_header())

        set_config.config.sink_id = self.sink_id
        set_config_rw(set_config.config, self.new_config)
        set_config_keys(set_config.config.keys, self.new_config)

        return message.SerializeToString()


class SetConfigResponse(Response):
    """
    SetConfigResponse: Response to answer a SetConfigRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        sink_id (str): id of the sink (dependant on gateway)
        config (dict): dictionnary containing the sink configuration after the setConfig request
    """

    def __init__(self, req_id, gw_id, res, sink_id, config, **kwargs):
        super(SetConfigResponse, self).__init__(req_id, gw_id, res, sink_id, **kwargs)
        # Config can be null in case of wrong sink_id for example
        self.config = config

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse SetConfigResponse payload")

        response = message.wirepas.set_config_resp

        d = Response._parse_response_header(response.header)

        if d["sink_id"] != response.config.sink_id:
            print("Error: Mismatch in sink id for set_config_response")

        new_config = {}
        new_config["sink_id"] = response.config.sink_id
        parse_config_ro(response.config, new_config)
        parse_config_rw(response.config, new_config)

        return cls(d["req_id"], d["gw_id"], d["res"], d["sink_id"], new_config)

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()

        response = message.wirepas.set_config_resp
        response.header.CopyFrom(self._make_response_header())

        response.config.sink_id = self.sink_id
        if self.config is not None:
            set_config_rw(response.config, self.config)
            set_config_ro(response.config, self.config)

        return message.SerializeToString()
