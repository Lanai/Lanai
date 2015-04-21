# -*-coding: utf8-*-

from lanai.app import Lanai
from lanai.server import LanaiServer
from lanai.protocol import Protocol

protocol = Protocol('ping-pong')


@protocol.event()
def on_ping(data):
    return dict(data='pong')

app = Lanai()
app.register_protocol(protocol)

server = LanaiServer(app)
server.serve_forever()