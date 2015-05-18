# -*- coding:utf-8 -*-
from redis import StrictRedis

from threading import local

redis_session = StrictRedis(host='localhost', port=6379, db=1)
shared_data = local()