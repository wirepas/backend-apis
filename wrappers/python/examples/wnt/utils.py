"""
    Utils
    =====

    Generic tools to handle tty commands and logging

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import sys
import json
import yaml
import logging
import argparse

from typing import Type


class Settings(object):
    """Simple class to handle library settings"""

    def __init__(self, settings):
        super(Settings, self).__init__()
        self.__dict__ = settings

    def __str__(self):
        return json.dumps(self)


def print_to_tty(message: dict) -> None:
    """ send message to stdout"""
    print(str(message))


def sort_dict(d: dict, reverse: bool = True):
    return [[k, d[k]] for k in sorted(d, key=d.get, reverse=reverse)]


def get_settings() -> Type[Settings]:
    args = parse_args()

    if args.settings:
        with open(args.settings, "r") as f:
            settings = yaml.safe_load(f)

    # overwrite file settings
    for key, value in args.__dict__.items():
        if value is not None:
            settings[key] = value

    settings = Settings(settings)

    return settings


def setup_log(module: str, level: str = "error"):
    """
    Prepares logging.

    Setups Python's logging and by default send up to LEVEL
    logs to stdout.

    Args:
        module (str): name to use in the logging
        level (str): logging level name (case insensitive)
    """

    logger = logging.getLogger(module)
    try:
        logger.setLevel(getattr(logging, level.upper()))
    except ValueError:
        logger.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        "{"
        '"level":"%(levelname)s", '
        '"module":"%(module)s", '
        '"function":"%(funcName)s", '
        '"Message":"%(message)s"'
        "}"
    )

    # configures stdout
    h = logging.StreamHandler(stream=sys.stdout)
    h.setFormatter(formatter)

    logger.addHandler(h)
    return logger


def parse_args():
    """Parse known command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example of a simple RPC client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--settings",
        type=str,
        required=False,
        default="./settings.yml",
        help="settings file.",
    )

    parser.add_argument(
        "--username",
        type=str,
        required=False,
        default=None,
        help="username to login with.",
    )

    parser.add_argument("--password", type=str, default=None, help="password for user.")

    parser.add_argument(
        "--hostname", default=None, type=str, help="domain where to point requests."
    )

    parser.add_argument(
        "--log_level",
        type=str,
        default="info",
        help="desired log level per defined in the std logging module.",
    )

    parser.add_argument(
        "--protocol_version", type=int, default=3, help="WS API protocol version."
    )

    parser.add_argument(
        "--message_format",
        type=str,
        default="json",
        help="which format to use in the return (json | proto).",
    )

    parser.add_argument(
        "--keep_alive",
        type=int,
        default=60,
        help="period to check if threads are running",
    )

    known, _ = parser.parse_known_args()

    return known
