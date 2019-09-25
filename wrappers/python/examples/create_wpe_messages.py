#!/usr/bin/env bash

import wirepas_messaging


def example_mesh_data():
    """ Creates an example mesh data message """
    meshdata = wirepas_messaging.wpe.MeshData()
    meshdata.sequence = 1
    meshdata.source = 1000

    return meshdata


if __name__ == "__main__":

    print(example_mesh_data())
