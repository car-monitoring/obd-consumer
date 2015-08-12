#!/bin/bash
set -e

CONF=/etc/obd-consumer/obd-consumer.conf

exec /usr/local/bin/obd-consumer-api
