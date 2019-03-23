import wirepas_messaging
from .default_value import *


def test_generate_parse_request():
    # Clear a scratchpad
    request = wirepas_messaging.gateway.api.ProcessScratchpadRequest(
        SINK_ID,
        REQUEST_ID
    )

    request2 = wirepas_messaging.gateway.api.ProcessScratchpadRequest.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_messaging.gateway.api.ProcessScratchpadResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID
    )

    request2 = wirepas_messaging.gateway.api.ProcessScratchpadResponse.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]