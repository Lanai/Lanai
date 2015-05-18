# -*- coding:utf-8 -*-
from __future__ import absolute_import

from .handlers import ConnectionHandler
from .utils import get_uuid


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

    def handle_timer(self,
                     protocol,
                     func,
                     seconds,
                     target_handlers,
                     is_broadcast):
        from gevent import sleep

        while True:
            if is_broadcast:
                target_handlers = self.connection_handler_info.values()
            for handler in target_handlers:
                data = func(handler)
                response_data = protocol.get_cleaned_response_data(
                    func.__name__, data
                )
                handler.send(response_data)
            sleep(seconds)