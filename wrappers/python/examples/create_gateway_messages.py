#!/usr/bin/env bash

import wirepas_messaging
import datetime


def example_received_packet():
    """ Creates an example received packet """
    received_packet = wirepas_messaging.gateway.PacketReceivedEvent()

    received_packet.source_address = 1000
    received_packet.destination_address = 20
    received_packet.destination_address = 20
    received_packet.source_endpoint = 10
    received_packet.destination_endpoint = 10
    received_packet.travel_time_ms = 3
    received_packet.rx_time_ms_epoch = int(datetime.datetime.now().timestamp() * 1e3)

    return received_packet


if __name__ == "__main__":

    print(example_received_packet())
