"""
    Send data
    =========

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .request import Request
from .response import Response

from .wirepas_exceptions import GatewayAPIParsingException


class SendDataRequest(Request):
    """
    SendDataRequest: request to send data from a given sink

    Attributes:
        dest_add(int): destination address
        src_ep(int): source endpoint
        dst_ep(int): destination endpoint
        qos(int): Wirepas QOS to use for this message
        payload(bytearray): the data to send
        initial_delay_ms(int): initial delay to add to travel time
        sink_id (str): id of the sink (dependant on gateway)
        req_id (int): unique request id
        is_unack_csma_ca(bool): if true only sent to CB-MAC nodes
        hop_limit(int): maximum number of hops this message can do to reach its destination (<16)
    """

    def __init__(
        self,
        dest_add,
        src_ep,
        dst_ep,
        qos,
        payload,
        initial_delay_ms=0,
        sink_id=None,
        req_id=None,
        is_unack_csma_ca=False,
        hop_limit=0,
        **kwargs
    ):
        super(SendDataRequest, self).__init__(sink_id, req_id, **kwargs)
        self.destination_address = dest_add
        self.source_endpoint = src_ep
        self.destination_endpoint = dst_ep
        self.qos = qos
        self.data_payload = payload
        self.initial_delay_ms = initial_delay_ms
        self.is_unack_csma_ca = is_unack_csma_ca
        self.hop_limit = hop_limit

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse SendDataRequest payload")

        req = message.wirepas.send_packet_req
        d = Request._parse_request_header(req.header)

        # Handle optional fields
        try:
            initial_delay_ms = req.initial_delay_ms
        except AttributeError:
            # Attribute is not defined
            initial_delay_ms = 0

        try:
            is_unack_csma_ca = req.is_unack_csma_ca
        except AttributeError:
            # Attribute is not defined
            is_unack_csma_ca = False

        try:
            hop_limit = req.hop_limit
        except AttributeError:
            # Attribute is not defined
            hop_limit = 0

        return cls(
            req.destination_address,
            req.source_endpoint,
            req.destination_endpoint,
            req.qos,
            req.payload,
            initial_delay_ms,
            d["sink_id"],
            d["req_id"],
            is_unack_csma_ca,
            hop_limit,
        )

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()

        # Fill the request header
        req = message.wirepas.send_packet_req
        req.header.CopyFrom(self._make_request_header())

        req.destination_address = self.destination_address
        req.source_endpoint = self.source_endpoint
        req.destination_endpoint = self.destination_endpoint
        req.qos = self.qos

        req.payload = self.data_payload
        if self.initial_delay_ms > 0:
            req.initial_delay_ms = self.initial_delay_ms

        if self.is_unack_csma_ca:
            # Only set the optional field if True
            req.is_unack_csma_ca = self.is_unack_csma_ca

        if self.hop_limit > 0:
            req.hop_limit = self.hop_limit

        return message.SerializeToString()


class SendDataResponse(Response):
    """
     SendDataResponse: Response to answer a SendDataRequest

     Attributes:
         req_id (int): unique request id that this Response is associated
         gw_id (str): gateway unique identifier
         res (GatewayResultCode): result of the operation
         sink_id (str): id of the sink (dependant on gateway)
     """

    def __init__(self, req_id, gw_id, res, sink_id, **kwargs):
        super(SendDataResponse, self).__init__(req_id, gw_id, res, sink_id, **kwargs)

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse SendDataResponse payload")

        response = message.wirepas.send_packet_resp

        d = Response._parse_response_header(response.header)

        return cls(d["req_id"], d["gw_id"], d["res"], d["sink_id"])

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()

        response = message.wirepas.send_packet_resp
        response.header.CopyFrom(self._make_response_header())

        return message.SerializeToString()
