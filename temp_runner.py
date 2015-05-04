# -*-coding: utf8-*-
import yaml

from lanai.app import Lanai
from lanai.server import LanaiServer
from lanai.protocol import Protocol
from lanai.utils import get_uuid

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

HOST = config['server']['host']
PORT = config['server']['port']

protocol = Protocol('ping-pong')


@protocol.event()
def on_ping(data):
    return dict()


@protocol.timer(3)
def ping(_app):
    print 'ping'
    return dict(id=get_uuid())


if __name__ == '__main__':
    app = Lanai()
    app.register_protocol(protocol)

    server = LanaiServer(app, HOST, PORT)
    server.serve_forever()
