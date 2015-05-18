# -*-coding: utf8-*-

import socket
import sys
import struct
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 1234)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


def read(_length):
    global sock
    _data = ''
    while len(_data) < _length:
        try:
            packet = sock.recv(_length - len(_data))
        except Exception:
            return
        if not packet:
            return
        _data = '%s%s' % (_data, packet)
    return _data


def send(_data):
    global sock
    _data = json.dumps(_data)
    _data = (struct.pack('>I', len(_data)) + _data)
    sock.sendall(_data)
    print >>sys.stderr, 'sending "%s"' % _data


while True:
    raw_data = read(4)
    length = struct.unpack('>I', raw_data)[0]
    data = read(length)
    print >>sys.stderr, 'received "%s"' % data
    data = json.loads(data)
    protocol = data.get('protocol', None)
    event = data.get('event', None)
    if protocol == 'ping-pong' and event == 'ping':
        ping_id = data['data'].get('id')
        send(dict(protocol=protocol, event='pong', data=dict(id=ping_id)))

