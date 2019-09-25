"""
    Get gateway info
    ================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .request import Request
from .response import Response

from .wirepas_exceptions import GatewayAPIParsingException


class GetGatewayInfoRequest(Request):
    """
    GetGatewayInfoRequest: Request to obtain the gateway config

    Attributes:
        req_id (int): unique request id
    """

    def __init__(self, req_id=None, **kwargs):
        super(GetGatewayInfoRequest, self).__init__(req_id=req_id, **kwargs)

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse GetGatewayInfoRequest payload"
            )

        d = Request._parse_request_header(message.wirepas.get_gateway_info_req.header)
        return cls(d["req_id"])

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()
        # Fill the request header
        get_gateway_info = message.wirepas.get_gateway_info_req
        get_gateway_info.header.CopyFrom(self._make_request_header())

        return message.SerializeToString()


class GetGatewayInfoResponse(Response):
    """
    GetGatewayInfoResponse: Response to answer a GetGatewayInfoRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        current_time_s_epoch (int): current timestamp in ms relative to epoch
        gateway_model (string): gateway model (managed by gateway integrator)
        gateway_version (string): gateway version (managed by gateway integrator)
    """

    def __init__(
        self,
        req_id,
        gw_id,
        res,
        current_time_s_epoch,
        gateway_model=None,
        gateway_version=None,
        implemented_api_version=None,
        **kwargs
    ):
        super(GetGatewayInfoResponse, self).__init__(req_id, gw_id, res, **kwargs)
        self.current_time_s_epoch = current_time_s_epoch
        self.gateway_model = gateway_model
        self.gateway_version = gateway_version
        self.implemented_api_version = implemented_api_version

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse GetGatewayInfoResponse payload"
            )

        response = message.wirepas.get_gateway_info_resp

        d = Response._parse_response_header(response.header)

        return cls(
            d["req_id"],
            d["gw_id"],
            d["res"],
            current_time_s_epoch=response.info.current_time_s_epoch,
            gateway_model=response.info.gw_model,
            gateway_version=response.info.gw_version,
            implemented_api_version=response.info.implemented_api_version,
        )

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()

        response = message.wirepas.get_gateway_info_resp
        response.header.CopyFrom(self._make_response_header())

        response.info.current_time_s_epoch = self.current_time_s_epoch

        if self.gateway_model is not None:
            response.info.gw_model = self.gateway_model

        if self.gateway_version is not None:
            response.info.gw_version = self.gateway_version

        if self.implemented_api_version is not None:
            response.info.implemented_api_version = self.implemented_api_version

        return message.SerializeToString()
