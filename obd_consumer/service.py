# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools
import time

import obd
import requests
import six

from obd_consumer import cache


MAX_RETRY_COUNT = 5
TIME_INTERVAL = 5
STATS_FREQUENCY = 6
# STATS_FREQUENCY = 0

_CONN = None

STATS_SUFIX_MAP = {
    "0104: Calculated Engine Load": "/metrics/api/engine_load/",
    "012F: Fuel Level Input": "/metrics/api/fuel_level/",
    "0103: Fuel System Status": "/metrics/api/fuel_status/",
    "0151: Fuel Type": "/metrics/api/fuel_type/",
    "010B: Intake Manifold Pressure": "/metrics/api/intake_pressure/",
    "010C: Engine RPM": "/metrics/api/rpm/",
    "010D: Vehicle Speed": "/metrics/api/speed/"
}


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


def push_to_server(command, value, unit):
    command = str(command)
    if command not in STATS_SUFIX_MAP:
        return

    config = six.moves.configparser.ConfigParser()
    config.read('/etc/obd-consumer.conf')

    url = config.get('DEFAULT', 'url')
    username = config.get('DEFAULT', 'username')
    password = config.get('DEFAULT', 'password')

    payload = {"username": username, "password": password}

    response = requests.post(url + '/api-token-auth/', data=payload)

    if not response.ok:
        return

    token = response.json()['token']
    header = {'Authorization': 'Token ' + token}
    data = {"value": value, "unit": unit}
    sufix = STATS_SUFIX_MAP[command]
    foo = requests.post(url + sufix, data=data, headers=header)


def consumer_service():
    x = 0
    while True:
        connection = get_connection()
        for command in connection.supported_commands:
            value, unit = fetch_data(command)
            cache.push_data(command, value, unit)
            print (command)

            if x == STATS_FREQUENCY:
                push_to_server(command, value, unit)
                x = 0
        x += 1

        time.sleep(TIME_INTERVAL)
