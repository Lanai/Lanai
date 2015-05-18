# -*- coding:utf-8 -*-
from __future__ import absolute_import

import json
import struct
import inspect

from socket import error as socket_error

from .connection import Connection
from .exceptions import (
    LanaiError,
    InvalidPacketError,
    InvalidProtocolError,
    InvalidEventError
)


class ConnectionHandler(object):

    def __init__(self, socket, address_set, app):
        self.connection = Connection(socket, address_set)
        self.app = app
        self.app.register_connection_handler(self)
        self.handle()

    def handle(self):
        while not self.connection.socket.closed:
            raw_data = self.read(4)
            if not raw_data:
                self.close()
                break
            length = struct.unpack('>I', raw_data)[0]
            packet = self.read(length)
            try:
                packet = json.loads(packet)
            except (ValueError, TypeError):
                message = "The type of packet must always json."
                self.error_response(InvalidPacketError(message=message))
            try:
                self.protocol_processor(packet)
            except LanaiError, e:
                self.error_response(e)

    def read(self, length):
        data = ''
        while len(data) < length:
            try:
                packet = self.connection.socket.recv(length - len(data))
            except socket_error:
                return
            if not packet:
                return
            data = '%s%s' % (data, packet)
        return data

    def send(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        else:
            # TODO invalid event response error
            return
        data = (struct.pack('>I', len(data)) + data)
        try:
            self.connection.socket.send(data)
        except socket_error:
            self.close()

    def close(self):
        from gevent import socket

        try:
            self.connection.socket.shutdown(socket.SHUT_WR)
            self.connection.socket.close()
        except socket_error:
            pass
        self.app.unregister_connection_handler(self.connection.id)

    def protocol_processor(self, packet):
        if packet is None:
            message = "The type of packet must always json."
            raise InvalidPacketError(message=message)

        self.connection.update()
        protocol_name = packet.get('protocol', '')
        protocol = self.app.protocol_info.get(protocol_name, None)
        if protocol is None:
            message = "'%s' protocol doesn't exits." % protocol_name
            raise InvalidProtocolError(message=message)

        event_name = packet.get('event', '')
        event_func = protocol.event_rule.get(event_name, None)
        if event_func is None:
            message = "'%s' event doesn't exits in %s protocol." % (event_name, protocol_name)
            raise InvalidEventError(message=message)
        data = packet.get('data', {})
        args_count = len(inspect.getargspec(event_func).args)
        if args_count >= 2:
            args = (self, data)
        else:
            args = (data,)
        response_data = event_func(*args)
        if response_data is not None:
            response_data = protocol.get_cleaned_response_data(
                event_name, response_data
            )
            self.send(response_data)

    def error_response(self, error):
        data = dict(status=dict(code=error.code, message=error.message))
        self.send(data)
