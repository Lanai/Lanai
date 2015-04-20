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


try:
    # Send data
    data = dict(protocol='ping-pong', event='ping')
    data = json.dumps(data)
    print >>sys.stderr, 'sending "%s"' % data
    data = (struct.pack('>I', len(data)) + data)
    sock.sendall(data)

    # Look for the response
    raw_data = read(4)
    length = struct.unpack('>I', raw_data)[0]
    data = read(length)
    print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()