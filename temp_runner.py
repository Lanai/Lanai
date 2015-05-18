# -*-coding: utf8-*-
import yaml

from lanai.app import Lanai
from lanai.server import LanaiServer
from lanai.protocol.ping_pong import protocol as ping_pong


with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

HOST = config['server']['host']
PORT = config['server']['port']


if __name__ == '__main__':
    app = Lanai()
    app.register_protocol(ping_pong)
    server = LanaiServer(app, HOST, PORT)
    print 'Server started on port {}'.format(PORT)
    server.serve_forever()
