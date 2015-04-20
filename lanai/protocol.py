# -*-coding: utf8-*-


class Protocol(object):

    def __init__(self, name):
        self.name = name
        self.event_rule = dict()

    def event(self):
        def decorator(f):
            name = f.__name__.replace('on_', '')
            self.event_rule[name] = f
        return decorator