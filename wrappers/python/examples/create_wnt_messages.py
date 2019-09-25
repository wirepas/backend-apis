#!/usr/bin/env bash

import wirepas_messaging


def example_neighbor():
    """ Creates an example neighbor message """
    neighbor = wirepas_messaging.wnt.Neighbor()

    neighbor.address = 1
    neighbor.cluster_channel_MHz = 2
    neighbor.radio_power_dB = 4
    neighbor.neighbor_type = wirepas_messaging.wnt.Neighbor.NeighborType.Value("MEMBER")
    neighbor.rssi_dBm = -56
    neighbor.no_neighbors = 1

    return neighbor


if __name__ == "__main__":

    print(example_neighbor())
