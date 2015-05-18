# -*- coding:utf-8 -*-
from lanai.utils import get_uuid
from lanai.protocol import Protocol
from lanai.globals import shared_data
from lanai.exceptions import InvalidDataError

from datetime import datetime

protocol = Protocol('ping-pong')

_dict_name = 'ping_info'
if not hasattr(shared_data, _dict_name):
    setattr(shared_data, _dict_name, dict())
ping_info = getattr(shared_data, _dict_name)


def get_ping_info_key(connection_id):
    return 'connection_%s' % connection_id


@protocol.timer(5)
def ping(handler):
    global ping_info

    ping_id = get_uuid()
    ping_info[get_ping_info_key(handler.connection.id)] = dict(
        id=ping_id,
        created_at=datetime.now()
    )
    return dict(id=ping_id)


@protocol.event
def on_pong(handler, data):
    global ping_info

    ping_id = data.get('id', None)
    if ping_id is None:
        raise InvalidDataError(message='Id of ping is required.')
    _ping = ping_info.get(get_ping_info_key(handler.connection.id), None)
    if _ping is None:
        raise InvalidDataError(message='Invalid event.')
    origin_id = _ping.get('id', None)
    if ping_id != origin_id:
        raise InvalidDataError(message='Invalid id of ping.')
    del ping_info['connection_%s' % handler.connection.id]


# TODO dead connection remove.