# -*-coding: utf8-*-
import yaml

from lanai.app import Lanai
from lanai.server import LanaiServer
from lanai.protocol import Protocol

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

protocol = Protocol('ping-pong')


@protocol.event()
def on_ping(data):
    return dict(data='pong')

app = Lanai()
app.register_protocol(protocol)

server = LanaiServer(app, config['server']['host'], config['server']['port'])
server.serve_forever()
