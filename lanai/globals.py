# -*- coding:utf-8 -*-
from redis import StrictRedis

redis_session = StrictRedis(host='localhost', port=6379, db=1)