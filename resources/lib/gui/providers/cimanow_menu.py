# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.media_menu import MediaMenu
from resources.lib.modules.providers.cimanow import Cimanow


class CimanowMenu(MediaMenu):
    def __init__(self):
        super().__init__()
        self.api = Cimanow()
