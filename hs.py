# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import sys

from resources.lib.modules import router
from resources.lib.modules.globals import g
from resources.lib.modules.timeLogger import TimeLogger

g.init_globals(sys.argv)

try:
    with TimeLogger('{}'.format(g.REQUEST_PARAMS.get('action', ''))):
        router.dispatch(g.REQUEST_PARAMS)
finally:
    g.deinit()
