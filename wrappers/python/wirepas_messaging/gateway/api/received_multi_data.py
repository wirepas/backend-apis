"""
    Received data
    =============

    .. Copyright:
        Copyright 2020 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging

from .event import Event
from .wirepas_exceptions import GatewayAPIParsingException


class ReceivedMultiDataEvent(Event):
    """
    ReceivedMultiDataEvent: Event generated when multiple messages are received
    and grouped together from Wirepas network

    Attributes:
        gw_id (str): gateway unique identifier (all grouped messages are from same gateway)
        event_id(int): event unique id (random value generated if None)
        packets(list of dictionary): all individual packets as a list of dictionary with following keys
                    sink_id (str): id of the sink (dependant on gateway)
                    rx_time_ms_epoch(int): timestamp in ms of message reception relative to epoch
                    source_address(int): source address
                    destination_address(int): destination address
                    source_endpoint(int): source endpoint
                    destination_endpoint(int): destination endpoint
                    travel_time_ms(int): travel time of the packet in the Wirepas network
                    qos(int): Wirepas QOS used by sender for this message
                    data_payload(bytearray): the received data or None if must be hidden
                    data_size(int): the received data size, only needed if data is None
                    hop_count(int): number of hop for the message to reach the gateway
    """

    def __init__(self, gw_id, packets, event_id=None, **kwargs):
        super(ReceivedMultiDataEvent, self).__init__(
            gw_id, sink_id=None, event_id=event_id, **kwargs
        )
        self.packets = packets

    @classmethod
    def from_payload(cls, payload):
        message = wirepas_messaging.gateway.GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse ReceivedDataEvent payload")

        event = message.wirepas.multi_packet_received_event
        d = Event._parse_event_header(event.header)

        packets = []

        for packet in event.packets:
            # Check hop count field
            try:
                hop_count = packet.hop_count
            except AttributeError:
                # Attribute is not defined
                hop_count = 0

            packet_dic = {
                "sink_id": packet.sink_id,
                "source_address": packet.source_address,
                "destination_address": packet.destination_address,
                "source_endpoint": packet.source_endpoint,
                "destination_endpoint": packet.destination_endpoint,
                "travel_time_ms": packet.travel_time_ms,
                "rx_time_ms_epoch": packet.rx_time_ms_epoch,
                "qos": packet.qos,
                "hop_count": hop_count,
            }

            # Check optional payload field
            if packet.HasField("payload"):
                packet_dic["data_payload"] = packet.payload

            # Check optional payload size field
            if packet.HasField("payload_size"):
                packet_dic["data_size"] = packet.payload_size

            packets.append(packet_dic)

        return cls(d["gw_id"], packets=packets, event_id=d["event_id"])

    @property
    def payload(self):
        message = wirepas_messaging.gateway.GenericMessage()
        # Fill the event header
        event = message.wirepas.multi_packet_received_event
        event.header.CopyFrom(self._make_event_header())

        for packet in self.packets:
            # Add a repeated field
            proto_packet = event.packets.add()

            # Fill the different fields
            proto_packet.sink_id = packet["sink_id"]
            proto_packet.source_address = packet["source_address"]
            proto_packet.destination_address = packet["destination_address"]
            proto_packet.source_endpoint = packet["source_endpoint"]
            proto_packet.destination_endpoint = packet["destination_endpoint"]
            proto_packet.travel_time_ms = packet["travel_time_ms"]
            proto_packet.rx_time_ms_epoch = packet["rx_time_ms_epoch"]
            proto_packet.qos = packet["qos"]

            try:
                data_payload = packet["data_payload"]
                if data_payload is not None:
                    proto_packet.payload = data_payload
            except KeyError:
                # Field is optional, just skip it
                pass

            try:
                data_size = packet["data_size"]
                if data_size is not None:
                    proto_packet.payload_size = data_size
            except KeyError:
                # Field is optional, just skip it
                pass

            if packet["hop_count"] > 0:
                proto_packet.hop_count = packet["hop_count"]

        return message.SerializeToString()
