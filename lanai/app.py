# -*- coding:utf-8 -*-
from lanai.handlers import ConnectionHandler


class Lanai(object):
    _default_config = dict(
        host='0.0.0.0',
        port=1234
    )
    protocol_rule = dict()

    def __init__(self, config=_default_config,
                 connection_handler_class=ConnectionHandler):
        self.config = config
        self.connection_handler_class = connection_handler_class

    def register_protocol(self, protocol):
        self.protocol_rule[protocol.name] = protocol