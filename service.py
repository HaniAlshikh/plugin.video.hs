# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import sqlite3
import sys
from random import randint

import xbmc

from resources.lib.modules.globals import g

from resources.lib.modules.plugin_monitor import PluginMonitor

g.init_globals(sys.argv)

g.log("##################  STARTING SERVICE  ######################")
g.log("### {} {}".format(g.ADDON_ID, g.VERSION))
g.log("### PLATFORM: {}".format(g.PLATFORM))
g.log("### SQLite: {}".format(sqlite3.sqlite_version))  # pylint: disable=no-member
g.log("### Detected Kodi Version: {}".format(g.KODI_VERSION))
g.log("#############  SERVICE ENTERED KEEP ALIVE  #################")

monitor = PluginMonitor()
try:
    g.wait_for_abort(30)  # Sleep for a half a minute to allow widget loads to complete.
    while not monitor.abortRequested():
        if not g.wait_for_abort(15):  # Sleep to make sure tokens refreshed during maintenance
            xbmc.executebuiltin(
                'RunPlugin("plugin://plugin.video.hs/?action=syncM3U")'
            )
        if g.wait_for_abort(60 * randint(13, 17)):
            break
finally:
    del monitor
    g.deinit()
