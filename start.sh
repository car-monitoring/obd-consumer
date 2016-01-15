#!/bin/bash
set -e

CONF=/etc/obd-consumer/obd-consumer.conf

sudo chown -R obd: /opt/obd-consumer

exec /var/lib/obd-consumer/venv/bin/obd-consumer
