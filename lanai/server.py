# -*- coding:utf-8 -*-
from gevent import sleep
from gevent.server import StreamServer


class LanaiServer(StreamServer):

    def __init__(self, app, host, port):
        super(LanaiServer, self).__init__(
            listener=(host, port),
            handle=app.connection_handler_class
        )
        self.app = app
        self.extra_spawn_funcs = []

    def do_handle(self, *args):
        args = args + (self.app,)
        super(LanaiServer, self).do_handle(*args)

    def serve_forever(self, *args, **kwargs):
        spawn = self._spawn
        if spawn is None:
            return
        spawn(self._redis_subscribe)
        for protocol in self.app.protocol_info.values():
            for rule in protocol.timer_rules:
                func_args = (
                    protocol,
                    rule['func'],
                    rule['seconds'],
                    rule['target_handlers'],
                    rule['is_broadcast'],
                )
                spawn(self.app.handle_timer, *func_args)
        super(LanaiServer, self).serve_forever(*args, **kwargs)

    def _redis_subscribe(self):
        import json

        from lanai.globals import redis_session
        from lanai.chat import channel_prefix
        from lanai.chat.channel import get_channel

        pubsub = redis_session.pubsub()
        pubsub.psubscribe('*')
        while pubsub.subscribed:
            message = pubsub.get_message()
            if message is not None:
                channel_name = message.get('channel', None)
                if channel_name is None:
                    continue
                channel_name = channel_name.replace(channel_prefix, '')
                try:
                    data = json.loads(message.get('data', None))
                except (TypeError, ValueError):
                    continue
                sender_connection_id = data.get('sender_connection_id', None)
                message = data.get('message', None)
                channel = get_channel(channel_name)
                if channel is not None:
                    data = dict(message=message)
                    channel.publish(data, sender_connection_id)
            else:
                sleep()