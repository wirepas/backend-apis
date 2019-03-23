import wirepas_messaging
from .default_value import *


def test_generate_parse_event():
    status = wirepas_messaging.gateway.api.StatusEvent(
        GATEWAY_ID,
        GATEWAY_STATE
    )

    status2 = wirepas_messaging.gateway.api.StatusEvent.from_payload(
        status.payload
    )

    for k,v in status.__dict__.items():
        assert v == status2.__dict__[k]