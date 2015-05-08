# -*- coding:utf-8 -*-
from lanai.protocol import Protocol
from lanai.globals import redis_session

from lanai.chat import channel_prefix
from lanai.chat.channel import get_channel

chat_protocol = Protocol('chat')


@chat_protocol.event
def on_subscribe(handler, data):
    channel_name = data.get('channel', None)
    if channel_name is None:
        # TODO No channel name error.
        return
    channel = get_channel(channel_name)
    channel.subscribe(handler)


@chat_protocol.event
def on_unsubscribe(handler, data):
    channel_name = data.get('channel', None)
    if channel_name is None:
        # TODO No channel name error.
        return
    channel = get_channel(channel_name)
    channel.unsubscribe(handler)


@chat_protocol.event
def on_publish(handler, data):
    import json

    channel_name = data.get('channel', None)
    message = data.get('message', None)
    data = json.dumps(
        dict(
            channel=channel_name,
            message=message,
            sender_connection_id=handler.connection.id
        )
    )
    redis_session.publish('%s%s' % (channel_prefix, channel_name), data)