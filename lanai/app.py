# -*- coding:utf-8 -*-
from lanai.handlers import ConnectionHandler


class Lanai(object):
    protocol_rule = dict()

    def __init__(self, connection_handler_class=ConnectionHandler):
        self.connection_handler_class = connection_handler_class

    def register_protocol(self, protocol):
        self.protocol_rule[protocol.name] = protocol
