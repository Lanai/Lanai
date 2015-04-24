# -*- coding:utf-8 -*-
from lanai.handlers import ConnectionHandler


class Lanai(object):
    protocol_info = dict()
    connection_handler_info = dict()

    def __init__(self, connection_handler_class=ConnectionHandler):
        self.connection_handler_class = connection_handler_class

    def register_protocol(self, protocol):
        self.protocol_info[protocol.name] = protocol

    def register_connection_handler(self, connection_handler):
        connection_id = connection_handler.connection.id
        self.connection_handler_info[connection_id] = connection_handler

    def unregister_connection_handler(self, connection_id):
        del self.connection_info[connection_id]
