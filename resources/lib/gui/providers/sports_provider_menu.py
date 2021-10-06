# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.provider_menu import ProviderMenu


class SportsMenu(ProviderMenu):
    def __init__(self):
        super().__init__()

    ######################################################
    # MENUS
    ######################################################

    def games(self):
        self._list_current_games()

    def _list_current_games(self):
        games_list = self.api.get_games_list()
        self.list_builder.movie_menu_builder(games_list)
