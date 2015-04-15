# -*- coding:utf-8 -*-
from lanai.handlers import ConnectionHandler


class Lanai(object):
    _default_config = dict(
        host='0.0.0.0',
        port=1234
    )

    def __init__(self, config=_default_config,
                 connection_handler_class=ConnectionHandler,
                 protocol_dict={}):
        self.config = config
        self.connection_handler_class = connection_handler_class
        self.protocol_dict = protocol_dict