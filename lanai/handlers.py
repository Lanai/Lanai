# -*- coding:utf-8 -*-
import json
import struct

from socket import error as socket_error

from lanai.connection import Connection
from lanai.exceptions import (
    LanaiError,
    InvalidPacketError,
    InvalidProtocolError,
    InvalidEventError
)


class ConnectionHandler(object):

    def __init__(self, socket, address_set, protocol_rule):
        self.connection = Connection(socket, address_set)
        self.protocol_rule = protocol_rule
        self.handle()

    def handle(self):
        while not self.connection.socket.closed:
            raw_data = self.read(4)
            if not raw_data:
                self.close()
                break
            length = struct.unpack('>I', raw_data)[0]
            data = self.read(length)
            try:
                data = json.loads(data)
            except (ValueError, TypeError):
                message = "The type of packet must always json."
                self.error_response(InvalidPacketError(message=message))
            try:
                self.protocol_processor(data)
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

    def protocol_processor(self, data):
        if data is None:
            message = "The type of packet must always json."
            raise InvalidPacketError(message=message)

        self.connection.update()
        protocol_name = data.get('protocol', '')
        protocol = self.protocol_rule.get(protocol_name, None)
        if protocol is None:
            message = "'%s' protocol doesn't exits." % protocol_name
            raise InvalidProtocolError(message=message)

        event_name = data.get('event', '')
        event_func = protocol.event_rule.get(event_name, None)
        if event_func is None:
            message = "'%s' event doesn't exits in %s protocol." % (event_name, protocol_name)
            raise InvalidEventError(message=message)
        response_data = event_func(data)
        self.send(response_data)

    def error_response(self, error):
        data = dict(status=dict(code=error.code, message=error.message))
        self.send(data)
