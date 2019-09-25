"""
    Upload scratchpad
    =================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .request import Request
from .response import Response
from .wirepas_exceptions import GatewayAPIParsingException


class UploadScratchpadRequest(Request):
    """
    UploadScratchpadRequest: request to process scratchpad on a given sink

    Attributes:
        sink_id (str): id of the sink to upload scratchpad
        req_id (int): unique request id
        scratchpad (bytearray): scratchpad to upload (None to clear scratchpad)
    """

    def __init__(self, seq, sink_id, req_id=None, scratchpad=None, **kwargs):
        super(UploadScratchpadRequest, self).__init__(sink_id, req_id, **kwargs)
        self.seq = seq
        self.scratchpad = scratchpad

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse UploadScratchpadRequest payload"
            )

        req = message.wirepas.upload_scratchpad_req

        d = Request._parse_request_header(req.header)
        if req.HasField("scratchpad"):
            scratchpad = req.scratchpad
        else:
            # Clear the scratchpad
            scratchpad = None

        return cls(req.seq, d["sink_id"], d["req_id"], scratchpad)

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()
        # Fill the request header
        req = message.wirepas.upload_scratchpad_req
        req.header.CopyFrom(self._make_request_header())

        req.seq = self.seq
        if self.scratchpad is not None:
            req.scratchpad = self.scratchpad

        return message.SerializeToString()


class UploadScratchpadResponse(Response):
    """
    UploadScratchpadResponse: Response to answer a UploadScratchpadRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        sink_id (str): id of the sink (dependant on gateway)
    """

    def __init__(self, req_id, gw_id, res, sink_id, **kwargs):
        super(UploadScratchpadResponse, self).__init__(
            req_id, gw_id, res, sink_id, **kwargs
        )

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse UploadScratchpadResponse payload"
            )

        response = message.wirepas.upload_scratchpad_resp

        d = Response._parse_response_header(response.header)

        return cls(d["req_id"], d["gw_id"], d["res"], d["sink_id"])

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()

        response = message.wirepas.upload_scratchpad_resp
        response.header.CopyFrom(self._make_response_header())

        return message.SerializeToString()
