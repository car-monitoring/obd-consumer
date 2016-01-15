# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools
import time

import obd
import six

from obd_consumer import cache


MAX_RETRY_COUNT = 5
TIME_INTERVAL = 5

_CONN = None


def get_connection():
    global _CONN
    if _CONN is None:
        _CONN = obd.OBD()
    return _CONN


def retry(f):
    """OBD sometimes returns empty objects. Just retrying usually works."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        for __ in six.moves.range(MAX_RETRY_COUNT):
            result = f(*args, **kwargs)
            if result.message is not None:
                return result
        print('Not supported')
        return None
    return wrapper


@retry
def execute_command(command):
    connection = get_connection()
    response = connection.query(command)
    return response


def fetch_data(command):
    response = execute_command(command)
    if response is not None:
        return response.value, response.unit
    return None, None


def consumer_service():
    while True:
        connection = get_connection()
        for command in connection.supported_commands:
            value, unit = fetch_data(command)
            cache.push_data(command, value, unit)
            print (command)


        time.sleep(TIME_INTERVAL)
