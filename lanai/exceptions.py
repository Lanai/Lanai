# -*- coding:utf-8 -*-
class LanaiError(Exception):

    def __init__(self, code=None, message=''):
        code = self.__class__.__name__ if not code else code
        super(LanaiError, self).__init__(message)
        self.code = code


class PacketParseError(LanaiError):
    pass


class ProtocolParseError(LanaiError):
    pass


class InvalidProtocolError(LanaiError):
    pass


class InvalidEventError(LanaiError):
    pass