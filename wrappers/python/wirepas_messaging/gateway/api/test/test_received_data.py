import wirepas_messaging
from .default_value import *


def test_generate_parse_event():
    status = wirepas_messaging.gateway.api.ReceivedDataEvent(
        GATEWAY_ID,
        SINK_ID,
        RX_TIME_MS_EPOCH,
        SOURCE_ADD,
        DESTINATION_ADD,
        SOURCE_EP,
        DESTINATION_EP,
        TRAVEL_TIME_MS,
        QOS,
        DATA_PAYLOAD,
        hop_count=HOP_COUNT
    )

    status2 = wirepas_messaging.gateway.api.ReceivedDataEvent.from_payload(
        status.payload
    )

    for k,v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_no_payload():
    status = wirepas_messaging.gateway.api.ReceivedDataEvent(
        GATEWAY_ID,
        SINK_ID,
        RX_TIME_MS_EPOCH,
        SOURCE_ADD,
        DESTINATION_ADD,
        SOURCE_EP,
        DESTINATION_EP,
        TRAVEL_TIME_MS,
        QOS,
        data=None,
        data_size=5,
        hop_count=HOP_COUNT
    )

    status2 = wirepas_messaging.gateway.api.ReceivedDataEvent.from_payload(
        status.payload
    )

    for k,v in status.__dict__.items():
        assert v == status2.__dict__[k]