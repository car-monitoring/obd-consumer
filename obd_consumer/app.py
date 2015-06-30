# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pyramid import config as pyramid_config


def get_app():
    """App object with routes."""
    config = pyramid_config.Configurator()
    app = config.make_wsgi_app()

    return app
