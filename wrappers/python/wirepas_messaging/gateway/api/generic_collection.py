"""
    Generic collection
    =============

    .. Copyright:
        Copyright 2020 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""
# flake8: noqa
from wirepas_messaging.gateway.api import *


class GenericCollection(object):
    """
    GenericCollection: collection of Generic message

    """

    field_to_class = {
        "status_event": StatusEvent,
        "get_configs_req": GetConfigsRequest,
        "get_configs_resp": GetConfigsResponse,
        "set_config_req": SetConfigRequest,
        "set_config_resp": SetConfigResponse,
        "send_packet_req": SendDataRequest,
        "send_packet_resp": SendDataResponse,
        "packet_received_event": ReceivedDataEvent,
        "get_scratchpad_status_req": GetScratchpadStatusRequest,
        "get_scratchpad_status_resp": GetScratchpadStatusResponse,
        "upload_scratchpad_req": UploadScratchpadRequest,
        "upload_scratchpad_resp": UploadScratchpadResponse,
        "process_scratchpad_req": ProcessScratchpadRequest,
        "process_scratchpad_resp": ProcessScratchpadResponse,
        "get_gateway_info_req": GetGatewayInfoRequest,
        "get_gateway_info_res": GetGatewayInfoResponse,
    }

    def __init__(self, generic_messages_list, **kwargs):
        self.generic_messages_list = generic_messages_list

    @classmethod
    def from_payload(cls, payload):
        message_collection = wirepas_messaging.gateway.GenericMessageCollection()
        try:
            message_collection.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse Generic payload collection")

        msgs_list = []
        for message in message_collection.generic:
            for field, class_holder in GenericCollection.field_to_class.items():
                if message.wirepas.HasField(field):
                    msgs_list.append(class_holder.from_generic_message(message))
                    break

        return cls(msgs_list)

    @property
    def payload(self):
        message_collection = wirepas_messaging.gateway.GenericMessageCollection()
        # Add all messages one by one
        for message in self.generic_messages_list:
            message_collection.generic.append(message.generic_message)

        return message_collection.SerializeToString()

    @property
    def messages(self):
        return self.generic_messages_list

    def add_message(self, message):
        self.generic_messages_list.append(message)
