# -*- coding:utf-8 -*-
import json
import struct

from socket import error as socket_error

from lanai.connection import Connection
from lanai.exceptions import LanaiError, PacketParseError


class ConnectionHandler(object):

    def __init__(self, socket, address_set, protocol_dict):
        self.connection = Connection(socket, address_set)
        self.protocol_dict = protocol_dict
        self.handle()

    def handle(self):
        while True:
            raw_data = self.read(4)
            if not raw_data:
                self.close()
                break
            length = struct.unpack('>I', raw_data)[0]
            data = self.read(length)
            try:
                data = json.loads(data)
            except ValueError, e:
                self.error_response(PacketParseError(e.message))
            try:
                # TODO protocol processing.
                pass
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
        data = (struct.pack('>I', len(data)) + data)
        self.connection.socket.send(data)

    def close(self):
        from gevent import socket

        try:
            self.connection.socket.shutdown(socket.SHUT_WR)
            self.connection.socket.close()
        except socket_error:
            pass

    def error_response(self, error):
        data = dict(status=dict(code=error.code, message=error.message))
        self.send(data)