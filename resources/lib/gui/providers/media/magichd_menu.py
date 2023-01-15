# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.media.media_menu import MediaMenu
from resources.lib.modules.providers.media.MagicHD import MagicHD


class MagicHDMenu(MediaMenu):
    def __init__(self):
        super().__init__()
        self.api = MagicHD()

