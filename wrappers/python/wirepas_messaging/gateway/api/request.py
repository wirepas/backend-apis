"""
    Request
    =======

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import random
import wirepas_messaging


class Request(object):
    """
    Request

    Attributes:
        sink_id(str): sink identifier
        req_id (int): identifier to help distinguish a response/request pair
    """

    # pylint: disable=unused-argument
    def __init__(self, sink_id=None, req_id=None, **kwargs):
        super(Request, self).__init__()
        self.sink_id = sink_id
        if req_id is None:
            req_id = random.getrandbits(64)
        self.req_id = req_id

    def __str__(self):
        return str(self.__dict__)

    @property
    def payload(self):
        """ Implement how to serialize child Event classes """
        raise NotImplementedError()

    def _make_request_header(self):
        """ Creates the generic messaging header """
        header = wirepas_messaging.gateway.RequestHeader()
        header.req_id = self.req_id

        if self.sink_id is not None:
            header.sink_id = str(self.sink_id)

        return header

    @staticmethod
    def _parse_request_header(header):
        """
        Parses the header details from a protobuff message

        Args:
            header (proto): proto buff message

        Returns:
            A dictionary with the header details
        """
        d = dict()
        d["req_id"] = header.req_id
        if header.HasField("sink_id"):
            d["sink_id"] = header.sink_id
        else:
            d["sink_id"] = None

        return d
