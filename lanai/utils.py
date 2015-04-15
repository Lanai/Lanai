# -*- coding:utf-8 -*-


def get_uuid():
    import uuid
    return str(uuid.uuid4()).replace('-', '')