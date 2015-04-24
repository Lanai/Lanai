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

    def do_handle(self, *args):
        args = args + (self.app,)
        super(LanaiServer, self).do_handle(*args)

    def serve_forever(self, *args, **kwargs):
        spawn = self._spawn
        if spawn is None:
            return
        for protocol in self.app.protocol_info.values():
            for rule in protocol.timer_rules:
                func_args = (
                    protocol,
                    rule['func'],
                    rule['seconds'],
                    rule['target_handlers'],
                    rule['is_broadcast'],
                )
                spawn(self._run_timer, *func_args)
        super(LanaiServer, self).serve_forever(*args, **kwargs)

    def _run_timer(self,
                   protocol,
                   func,
                   seconds,
                   target_handlers,
                   is_broadcast):
        while True:
            if is_broadcast:
                target_handlers = self.app.connection_handler_info.values()
            for handler in target_handlers:
                data = func(self.app)
                response_data = protocol.default_response_data(func.__name__, data)
                handler.send(response_data)
            sleep(seconds)