# flake8: noqa

import wirepas_messaging
from default_value import *

message1 = {
    "sink_id": SINK_ID,
    "source_address": SOURCE_ADD,
    "destination_address": DESTINATION_ADD,
    "source_endpoint": SOURCE_EP,
    "destination_endpoint": DESTINATION_EP,
    "travel_time_ms": TRAVEL_TIME_MS,
    "rx_time_ms_epoch": RX_TIME_MS_EPOCH,
    "qos": QOS,
    "hop_count": HOP_COUNT,
    "data_payload": bytes(b"Message1"),
}

message2 = {
    "sink_id": SINK_ID,
    "source_address": SOURCE_ADD,
    "destination_address": DESTINATION_ADD,
    "source_endpoint": SOURCE_EP,
    "destination_endpoint": DESTINATION_EP,
    "travel_time_ms": TRAVEL_TIME_MS,
    "rx_time_ms_epoch": RX_TIME_MS_EPOCH,
    "qos": QOS,
    "hop_count": HOP_COUNT,
    "data_payload": bytes(b"Message2"),
}


def test_generate_parse_multi_packet():
    event = wirepas_messaging.gateway.api.ReceivedMultiDataEvent(
        GATEWAY_ID, [message1, message2]
    )

    event2 = wirepas_messaging.gateway.api.ReceivedMultiDataEvent.from_payload(
        event.payload
    )

    for k, v in event.__dict__.items():
        assert v == event2.__dict__[k]


def test_generate_parse_single_packet_in_multi_container():
    event = wirepas_messaging.gateway.api.ReceivedMultiDataEvent(GATEWAY_ID, [message1])

    event2 = wirepas_messaging.gateway.api.ReceivedMultiDataEvent.from_payload(
        event.payload
    )

    for k, v in event.__dict__.items():
        assert v == event2.__dict__[k]
