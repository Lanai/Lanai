# -*-coding: utf8-*-

import socket
import sys
import struct
import json
from multiprocessing import Process


def chat(i):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1234)
    sock.connect(server_address)
    # Send data
    data = dict(protocol='chat', event='subscribe', data=dict(channel='test'))
    send(sock, data)
    print >>sys.stderr, 'Task[%d] - sending "%s"' % (i, data)
    data = dict(protocol='chat', event='publish', data=dict(channel='test', message='test'))
    send(sock, data)
    print >>sys.stderr, 'Task[%d] - sending "%s"' % (i, data)

    while True:
        raw_data = read(sock, 4)
        length = struct.unpack('>I', raw_data)[0]
        data = read(sock, length)
        print >>sys.stderr, 'Task[%d] - received "%s"' % (i, data)


def read(_sock, _length):
    _data = ''
    while len(_data) < _length:
        try:
            packet = _sock.recv(_length - len(_data))
        except Exception:
            return
        if not packet:
            return
        _data = '%s%s' % (_data, packet)
    return _data


def send(_sock, _data):
    _data = json.dumps(_data)
    _data = (struct.pack('>I', len(_data)) + _data)
    _sock.sendall(_data)

ps = [Process(target=chat, args=(i,)) for i in xrange(3)]
for p in ps:
    p.start()