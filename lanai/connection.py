# -*- coding:utf-8 -*-
from datetime import datetime

from .utils import get_uuid


class Connection(object):

    def __init__(self, socket, address_set):
        self.id = get_uuid()
        self.socket = socket
        self.ip = address_set[0]
        self.port = address_set[1]
        self.created_at = datetime.now()
        self.updated_at = None

    def update(self):
        self.updated_at = datetime.now()