# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


import datetime

import xbmcgui

from resources.lib.common import tools
# from resources.lib.database.searchHistory import SearchHistory

from resources.lib.gui.menus import Menus
from resources.lib.modules.globals import g
from resources.lib.modules.list_builder import ListBuilder

from resources.lib.modules.providers.shahed4u import Shahed4u
from resources.lib.modules.providers.yallalive import Yallalive


class YallaliveMenus(Menus):
    def __init__(self):
        super().__init__()
        self.api = Yallalive()
        self.list_builder = ListBuilder()

    ######################################################
    # MENUS
    ######################################################

    def games(self):
        self._list_current_games()

    def _list_current_games(self):
        games_list = self.api.get_games_list()
        self.list_builder.movie_menu_builder(games_list)
