import wirepas_messaging
from .default_value import *

DUMMY_CONFIGS = [NODE_CONFIG_1]


def test_generate_parse_request():
    request = wirepas_messaging.gateway.api.GetConfigsRequest(
        REQUEST_ID
    )

    request2 = wirepas_messaging.gateway.api.GetConfigsRequest.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_messaging.gateway.api.GetConfigsResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        DUMMY_CONFIGS
    )

    request2 = wirepas_messaging.gateway.api.GetConfigsResponse.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]