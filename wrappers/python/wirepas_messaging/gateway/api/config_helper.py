"""
    Config Helper
    =============

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging


def convert_proto_role_to_wirepas(base, flags):
    """
    Maps the proto role enum to the correct Wirepas Mesh role

    Args:
        base (enum): protocol buffer enum
        flags (enum): protocol buffer enum

    Returns:
        Wirepas role as an int
    """
    base_proto_to_wirepas = dict(
        [
            (wirepas_messaging.gateway.NodeRole.SINK, 1),
            (wirepas_messaging.gateway.NodeRole.ROUTER, 2),
            (wirepas_messaging.gateway.NodeRole.NON_ROUTER, 3),
        ]
    )

    flag_proto_to_wirepas = dict(
        [
            (wirepas_messaging.gateway.NodeRole.LOW_LATENCY, 0x10),
            (wirepas_messaging.gateway.NodeRole.AUTOROLE, 0x80),
        ]
    )

    wirepas_role = base_proto_to_wirepas[base]

    for flag in flags:
        wirepas_role += flag_proto_to_wirepas[flag]

    return wirepas_role


def convert_wirepas_role_to_proto(wirepas_role):
    """
    Maps a Wirepas role to a protobuff enum

    Args:
        wirepas_role (int): device role in WM network

    Returns:
        Tupple with protocol buffer base and flags
    """
    wirepas_base = wirepas_role & 0xF

    wirepas_base_to_proto = dict(
        [
            (1, wirepas_messaging.gateway.NodeRole.SINK),
            (2, wirepas_messaging.gateway.NodeRole.ROUTER),
            (3, wirepas_messaging.gateway.NodeRole.NON_ROUTER),
        ]
    )

    flag_proto_to_wirepas = dict(
        [
            (0x10, wirepas_messaging.gateway.NodeRole.LOW_LATENCY),
            (0x80, wirepas_messaging.gateway.NodeRole.AUTOROLE),
        ]
    )

    base = wirepas_base_to_proto[wirepas_base]

    flags = []
    flags_val = wirepas_role & 0xF0
    for flag in flag_proto_to_wirepas:
        if flag & flags_val != 0:
            flags.append(flag_proto_to_wirepas[flag])

    return base, flags


def parse_optional_field(message_obj, field, dic, key):
    """
    Copies attribute into dic if it exists in the proto message

    Args:
        message_obj (proto): protocol buffer object
        field (str): the field to test for existence in message_obj
        dic (dict): the dictionary where to copy the value into
        key (str): the dictionary key to use

    """

    if message_obj.HasField(field):
        dic[key] = getattr(message_obj, field)


def set_optional_field(message_obj, field, dic, key):
    """
    Sets field in the protocol buffer object. If the object does not
    accept it or if the key is not in dic the error is ignored.

    Args:
        message_obj (proto): protocol buffer object
        field (str): the field to test for existence in message_obj
        dic (dict): the dictionary where to copy the value into
        key (str): the dictionary key to use

    """

    try:
        setattr(message_obj, field, dic[key])
    except KeyError:
        # Field is unknown, just skip it
        pass


def parse_config_rw(message_obj, dic):
    """
    Parses the message_obj for read and write (rw) fields and copies them into
    dic.

    Args:
        message_obj (proto): protocol buffer object
        dic (dict): the dictionary where to copy the rw fields

    """

    if message_obj.HasField("node_role"):
        dic["node_role"] = convert_proto_role_to_wirepas(
            message_obj.node_role.role, message_obj.node_role.flags
        )

    parse_optional_field(message_obj, "node_address", dic, "node_address")
    parse_optional_field(message_obj, "network_address", dic, "network_address")
    parse_optional_field(message_obj, "network_channel", dic, "network_channel")
    parse_optional_field(
        message_obj.app_config, "diag_interval_s", dic, "app_config_diag"
    )
    parse_optional_field(message_obj.app_config, "seq", dic, "app_config_seq")
    parse_optional_field(
        message_obj.app_config, "app_config_data", dic, "app_config_data"
    )
    parse_optional_field(message_obj, "channel_map", dic, "channel_map")

    if message_obj.HasField("sink_state"):
        dic["started"] = message_obj.sink_state == wirepas_messaging.gateway.ON


def set_config_rw(message_obj, dic):
    """
    Sets the message_obj with the read and write (rw) fields present in dic.

    Args:
        message_obj (proto): protocol buffer object
        dic (dict): the dictionary where to copy the rw fields from

    """
    try:
        base, flags = convert_wirepas_role_to_proto(dic["node_role"])
        message_obj.node_role.role = base
        message_obj.node_role.flags.extend(flags)
    except KeyError:
        # Field is unknown, just skip it
        pass

    set_optional_field(message_obj, "node_address", dic, "node_address")
    set_optional_field(message_obj, "network_address", dic, "network_address")
    set_optional_field(message_obj, "network_channel", dic, "network_channel")

    set_optional_field(
        message_obj.app_config, "diag_interval_s", dic, "app_config_diag"
    )
    set_optional_field(message_obj.app_config, "seq", dic, "app_config_seq")

    try:
        message_obj.app_config.app_config_data = bytes(dic["app_config_data"])
    except KeyError:
        # Field is unknown, just skip it
        pass

    set_optional_field(message_obj, "channel_map", dic, "channel_map")

    try:
        if dic["started"]:
            message_obj.sink_state = wirepas_messaging.gateway.ON
        else:
            message_obj.sink_state = wirepas_messaging.gateway.OFF
    except KeyError:
        # Field is unknown, just skip it
        pass


def parse_config_keys(message_obj, dic):
    """
    Parses network keys.

    The keys are only available on a SinkNewConfig message.

    Args:
        message_obj (proto): protocol buffer object
        dic (dict): the dictionary where to copy the keys into
    """

    parse_optional_field(message_obj.keys, "cipher", dic, "cipher_key")
    parse_optional_field(message_obj.keys, "authentication", dic, "authentication_key")


def set_config_keys(message_obj, dic):
    """
    Sets network keys.

    The keys are only available on a SinkNewConfig message.

    Args:
        message_obj (proto): protocol buffer object
        dic (dict): the dictionary where to copy the keys from
    """
    set_optional_field(message_obj, "cipher", dic, "cipher_key")
    set_optional_field(message_obj, "authentication", dic, "authentication_key")


def parse_config_ro(message_obj, dic):
    """
    Sets the message_obj with the read only (ro) fields present in dic.

    Args:
        message_obj (proto): protocol buffer object
        dic (dict): the dictionary where to copy the ro fields from

    """
    parse_optional_field(
        message_obj.current_ac_range, "min_ms", dic, "current_ac_range_min"
    )
    parse_optional_field(
        message_obj.current_ac_range, "max_ms", dic, "current_ac_range_max"
    )

    parse_optional_field(message_obj.ac_limits, "min_ms", dic, "min_ac")
    parse_optional_field(message_obj.ac_limits, "max_ms", dic, "max_ac")

    parse_optional_field(message_obj, "max_mtu", dic, "max_mtu")

    parse_optional_field(message_obj.channel_limits, "min_channel", dic, "min_ch")
    parse_optional_field(message_obj.channel_limits, "max_channel", dic, "max_ch")
    parse_optional_field(message_obj, "hw_magic", dic, "hw_magic")
    parse_optional_field(message_obj, "stack_profile", dic, "stack_profile")
    parse_optional_field(message_obj, "app_config_max_size", dic, "app_config_max_size")
    parse_optional_field(message_obj, "are_keys_set", dic, "are_keys_set")

    if message_obj.HasField("firmware_version"):
        dic["firmware_version"] = [
            message_obj.firmware_version.major,
            message_obj.firmware_version.minor,
            message_obj.firmware_version.maint,
            message_obj.firmware_version.dev,
        ]


def set_config_ro(message_obj, dic):
    """
    Sets the message_obj with the read only (ro) fields present in dic.

    Args:
        message_obj (proto): protocol buffer object
        dic (dict): the dictionary where to copy the ro fields from

    """
    set_optional_field(message_obj.current_ac_range, "min_ms", dic, "min_ac_cur")
    set_optional_field(message_obj.current_ac_range, "max_ms", dic, "max_ac_cur")

    set_optional_field(message_obj.ac_limits, "min_ms", dic, "min_ac")
    set_optional_field(message_obj.ac_limits, "max_ms", dic, "max_ac")

    set_optional_field(message_obj, "max_mtu", dic, "max_mtu")

    set_optional_field(message_obj.channel_limits, "min_channel", dic, "min_ch")
    set_optional_field(message_obj.channel_limits, "max_channel", dic, "max_ch")

    set_optional_field(message_obj, "hw_magic", dic, "hw_magic")
    set_optional_field(message_obj, "stack_profile", dic, "stack_profile")
    set_optional_field(message_obj, "app_config_max_size", dic, "app_config_max_size")
    set_optional_field(message_obj, "are_keys_set", dic, "are_keys_set")

    try:
        message_obj.firmware_version.major = dic["firmware_version"][0]
        message_obj.firmware_version.minor = dic["firmware_version"][1]
        message_obj.firmware_version.maint = dic["firmware_version"][2]
        message_obj.firmware_version.dev = dic["firmware_version"][3]
    except KeyError:
        # Field is unknown, just skip it
        pass
