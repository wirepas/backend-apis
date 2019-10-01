"""
    Event
    =====

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""
import random
import wirepas_messaging


class Event(object):
    """
    Event

    Attributes:
        gw_id (str): gateway unique identifier
        sink_id(str): sink identifier
        event_id(int): event unique id (random value generated if None)
    """

    # pylint: disable=unused-argument
    def __init__(self, gw_id, sink_id=None, event_id=None, **kwargs):

        super(Event, self).__init__()
        self.gw_id = gw_id
        self.sink_id = sink_id
        if event_id is None:
            event_id = random.getrandbits(64)
        self.event_id = event_id

    def __str__(self):
        return str(self.__dict__)

    @property
    def payload(self):
        """ Implement how to serialize child Event classes """
        raise NotImplementedError()

    def _make_event_header(self):
        """ Creates the generic messaging header """
        header = wirepas_messaging.gateway.EventHeader()
        header.gw_id = str(self.gw_id)
        header.event_id = self.event_id

        if self.sink_id is not None:
            header.sink_id = str(self.sink_id)

        return header

    @staticmethod
    def _parse_event_header(header):
        """
        Parses the header details from a protobuff message

        Args:
            header (proto): proto buff message

        Returns:
            A dictionary with the header details
        """

        d = dict()
        d["gw_id"] = header.gw_id
        d["event_id"] = header.event_id
        if header.HasField("sink_id"):
            d["sink_id"] = header.sink_id
        else:
            d["sink_id"] = None

        return d
