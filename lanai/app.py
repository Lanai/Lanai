# -*- coding:utf-8 -*-
from lanai.handlers import ConnectionHandler
from lanai.utils import get_uuid


class Lanai(object):

    def __init__(self, connection_handler_class=ConnectionHandler):
        self.id = get_uuid()
        self.protocol_info = dict()
        self.connection_handler_info = dict()
        self.connection_handler_class = connection_handler_class

    def register_protocol(self, protocol):
        self.protocol_info[protocol.name] = protocol

    def register_connection_handler(self, connection_handler):
        connection_id = connection_handler.connection.id
        self.connection_handler_info[connection_id] = connection_handler

    def unregister_connection_handler(self, connection_id):
        del self.connection_handler_info[connection_id]