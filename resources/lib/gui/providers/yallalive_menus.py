# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.sports_provider_menu import SportsMenu
from resources.lib.modules.providers.yallalive import Yallalive


class YallaliveMenu(SportsMenu):
    def __init__(self):
        super().__init__()
        self.api = Yallalive()
