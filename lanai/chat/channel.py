# -*- coding:utf-8 -*-
from lanai.chat import protocol_name, channel_prefix
from lanai.chat.globals import channels


def get_channel(channel_name):
    if channel_name is None:
        return None
    if hasattr(channels, channel_name):
        return getattr(channels, channel_name)
    else:
        c = Channel(channel_name)
        setattr(channels, channel_name, c)
        return c


class Channel(object):

    def __init__(self, name):
        from lanai.globals import redis_session

        self.name = name
        self.connection_handlers = []
        pubsub = redis_session.pubsub()
        pubsub.subscribe('%s%s' % (channel_prefix, name))

    def subscribe(self, handler):
        if handler in self.connection_handlers:
            # TODO raise Already exist.
            pass
        else:
            self.connection_handlers.append(handler)

    def unsubscribe(self, handler):
        if handler in self.connection_handlers:
            self.connection_handlers.remove(handler)
        else:
            # TODO raise Not subscribed
            pass

    def publish(self, data, sender_connection_id=None):
        packet = dict(
            protocol=protocol_name,
            event='message',
            data=dict(channel=self.name)
        )
        if sender_connection_id is not None:
            packet['data']['sender_connection_id'] = sender_connection_id
        packet['data'].update(data)
        for handler in self.connection_handlers:
            handler.send(packet)