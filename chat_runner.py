# -*-coding: utf8-*-
import yaml

from lanai.app import Lanai
from lanai.server import LanaiServer
from lanai.chat.protocol import chat_protocol

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

HOST = config['server']['host']
PORT = config['server']['port']

if __name__ == '__main__':
    app = Lanai()
    app.register_protocol(chat_protocol)
    server = LanaiServer(app, HOST, PORT)
    print 'Server started on port {}'.format(PORT)
    server.serve_forever()
