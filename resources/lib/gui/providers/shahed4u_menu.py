# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.media_menu import MediaMenu
from resources.lib.modules.providers.shahed4u import Shahed4u


class Shahed4uMenu(MediaMenu):
    def __init__(self):
        super().__init__()
        self.api = Shahed4u()

