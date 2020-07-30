# flake8: noqa

from wirepas_messaging.gateway.api import *
from default_value import *


def test_generate_parse_collection():

    event1 = ReceivedDataEvent(
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
        hop_count=HOP_COUNT,
    )

    event2 = ReceivedDataEvent(
        GATEWAY_ID,
        SINK_ID,
        RX_TIME_MS_EPOCH + 10,
        SOURCE_ADD,
        DESTINATION_ADD,
        SOURCE_EP,
        DESTINATION_EP,
        TRAVEL_TIME_MS,
        QOS,
        DATA_PAYLOAD,
        hop_count=HOP_COUNT,
    )

    message_list = [event1, event2]

    collection = GenericCollection(message_list)

    collection2 = GenericCollection.from_payload(collection.payload)

    for message in collection2.messages:
        assert isinstance(message, ReceivedDataEvent)
