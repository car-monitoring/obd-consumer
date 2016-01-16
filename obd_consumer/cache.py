# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools
import json

import redis


def redis_conn(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        conn = redis.StrictRedis(host='localhost',
                                 port=6379,
                                 db=0)
        return f(conn, *args, **kwargs)
    return wrapper


@redis_conn
def push_data(conn, metric_name, value, unit):
    conn.hset(metric_name, 'value', value)
    conn.hset(metric_name, 'unit', unit)


@redis_conn
def push_supported_commands(conn, supported_commands):
    supported_commands = [
        str(command) for command in supported_commands
    ]
    conn.set('supported_commands', json.dumps(supported_commands))
