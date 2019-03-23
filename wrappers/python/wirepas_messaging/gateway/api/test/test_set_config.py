import wirepas_messaging
from .default_value import *


def test_generate_parse_request():
    request = wirepas_messaging.gateway.api.SetConfigRequest(
        SINK_ID,
        NODE_CONFIG_1,
        REQUEST_ID
    )

    request2 = wirepas_messaging.gateway.api.SetConfigRequest.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_messaging.gateway.api.SetConfigResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID,
        NODE_CONFIG_1
    )

    request2 = wirepas_messaging.gateway.api.SetConfigResponse.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]