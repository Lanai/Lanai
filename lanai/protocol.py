# -*- coding:utf-8 -*-


class Protocol(object):

    def __init__(self, name):
        self.name = name
        self.event_rule = dict()
        self.timer_rules = []

    def event(self, f):
        name = f.__name__.replace('on_', '')
        self.event_rule[name] = f

    def timer(self, seconds, target_handlers=[], is_broadcast=True):
        def decorator(f):
            self.timer_rules.append(dict(
                func=f,
                seconds=seconds,
                target_handlers=target_handlers,
                is_broadcast=is_broadcast
            ))
        return decorator

    def default_response_data(self, event_name, data):
        return dict(protocol=self.name, event_name=event_name, data=data)
