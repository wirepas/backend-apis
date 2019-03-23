import wirepas_messaging
from .default_value import *


def test_generate_parse_request():
    request = wirepas_messaging.gateway.api.SendDataRequest(
        DESTINATION_ADD,
        SOURCE_EP,
        DESTINATION_EP,
        QOS,
        DATA_PAYLOAD,
        INITIAL_DELAY,
        SINK_ID,
        REQUEST_ID,
        hop_limit=HOP_COUNT,
        is_unack_csma_ca=True
    )

    request2 = wirepas_messaging.gateway.api.SendDataRequest.from_payload(
        request.payload
    )

    for k,v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    response = wirepas_messaging.gateway.api.SendDataResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID
    )

    response2 = wirepas_messaging.gateway.api.SendDataResponse.from_payload(
        response.payload
    )

    for k,v in response.__dict__.items():
        assert v == response2.__dict__[k]