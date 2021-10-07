# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.media.media_menu import MediaMenu
from resources.lib.modules.providers.media.arabseed import Arabseed


class ArabseedMenu(MediaMenu):
    def __init__(self):
        super().__init__()
        self.api = Arabseed()
