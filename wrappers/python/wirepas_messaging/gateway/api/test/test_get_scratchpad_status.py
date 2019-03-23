import wirepas_messaging
from .default_value import *


def test_generate_parse_request():
    # Clear a scratchpad
    request = wirepas_messaging.gateway.api.GetScratchpadStatusRequest(
        SINK_ID,
        REQUEST_ID
    )

    request2 = wirepas_messaging.gateway.api.GetScratchpadStatusRequest.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_messaging.gateway.api.GetScratchpadStatusResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID,
        SCRATCHPAD_INFO,
        SCRATCHPAD_STATUS,
        SCRATCHPAD_TYPE,
        SCRATCHPAD_INFO,
        FIRMWARE_AREA_ID
    )

    request2 = wirepas_messaging.gateway.api.GetScratchpadStatusResponse.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        if isinstance(v, enum.Enum):
            assert v.value == request2.__dict__[k].value
        else:
            assert v == request2.__dict__[k]