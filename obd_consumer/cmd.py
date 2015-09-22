# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from wsgiref import simple_server

from obd_consumer import app
from obd_consumer import service


def api():
    """Console script for serving API."""
    server = simple_server.make_server('0.0.0.0', 8081, app.get_app())
    server.serve_forever()


def consumer():
    """Console script for consumer of OBD responses."""
    service.consumer_service()
