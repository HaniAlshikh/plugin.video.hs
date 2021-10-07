# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.sports.sports_menu import SportsMenu
from resources.lib.modules.providers.sports.asgoal import Asgoal


class AsgoalMenu(SportsMenu):
    def __init__(self):
        super().__init__()
        self.api = Asgoal()
