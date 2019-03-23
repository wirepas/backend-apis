import wirepas_messaging

from ..otap_helper import *


# Define list of default values used during testing
GATEWAY_ID = "test_gateway"
GATEWAY_STATE = wirepas_messaging.gateway.api.GatewayState.ONLINE
SINK_ID = "sink3"
RES_OK = wirepas_messaging.gateway.api.GatewayResultCode.GW_RES_OK
RES_KO = wirepas_messaging.gateway.api.GatewayResultCode.GW_RES_INTERNAL_ERROR
REQUEST_ID = 1234567
DESTINATION_ADD = 5678
SOURCE_ADD = 1234
SOURCE_EP = 98
DESTINATION_EP = 127
QOS = 0
DATA_PAYLOAD = bytes(b'Test')
INITIAL_DELAY = 12
RX_TIME_MS_EPOCH = int(123456789)
TRAVEL_TIME_MS = 123
HOP_COUNT = 10

# Todo add more fields in config
NODE_CONFIG_1 = dict([
    ('sink_id', SINK_ID),
    ('node_address', 123)
])

SCRATCHPAD_SEQ = 12
SCRATCHPAD = bytes(bytearray(1024))

SCRATCHPAD_INFO = dict([
    ('len', 2032),
    ('crc', 0x1234),
    ('seq', 112)
])

SCRATCHPAD_STATUS = ScratchpadStatus.SCRATCHPAD_STATUS_SUCCESS
SCRATCHPAD_TYPE = ScratchpadType.SCRATCHPAD_TYPE_PRESENT
FIRMWARE_AREA_ID = 0x123456
