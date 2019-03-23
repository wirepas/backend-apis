import wirepas_messaging
from .default_value import *
import time

def test_generate_parse_request():
    request = wirepas_messaging.gateway.api.GetGatewayInfoRequest(
        REQUEST_ID
    )

    request2 = wirepas_messaging.gateway.api.GetGatewayInfoRequest.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_messaging.gateway.api.GetGatewayInfoResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        int(time.time()),
        "Gateway model A",
        "Version x.y"
    )

    request2 = wirepas_messaging.gateway.api.GetGatewayInfoResponse.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]