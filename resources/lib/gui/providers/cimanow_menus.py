# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.menus import Menus
from resources.lib.modules.globals import g
from resources.lib.modules.list_builder import ListBuilder
from resources.lib.modules.providers.cimanow import Cimanow


class CimanowMenus(Menus):
    def __init__(self):
        super().__init__()
        self.api = Cimanow()
        self.list_builder = ListBuilder()

    ######################################################
    # MENUS
    ######################################################

    def movies(self, category: str = None):
        if category:
            self._list_movies_of_category(category)
        else:
            self._list_movies_categories()

    def _list_movies_of_category(self, category: str):
        movies_list = self.api.get_movies_list(category)
        self.list_builder.movie_menu_builder(movies_list)

    def _list_movies_categories(self):
        categories = self.api.get_movies_categories()
        for cat in categories:
            g.add_directory_item(
                cat,
                action="movies",
                action_args={"provider": self.api.name},
                category=cat,
            )
        g.close_directory(g.CONTENT_FOLDER)

    def shows(self, category: str = None):
        if category:
            self._list_shows_of_category(category)
        else:
            self._list_shows_categories()

    def _list_shows_of_category(self, category: str):
        shows_list = self.api.get_shows_list(category)
        self.list_builder.show_list_builder(shows_list)

    def _list_shows_categories(self):
        categories = self.api.get_shows_categories()
        for cat in categories:
            g.add_directory_item(
                cat,
                action="shows",
                action_args={"provider": self.api.name},
                category=cat,
            )
        g.close_directory(g.CONTENT_FOLDER)

    def show_seasons(self, url: str):
        seasons_list = self.api.get_shows_seasons(url)
        if not seasons_list:
            return self.episodes(url)
        self.list_builder.season_list_builder(seasons_list)

    def episodes(self, url: str):
        episodes_list = self.api.get_season_episodes(url)
        self.list_builder.episode_list_builder(episodes_list)

    def sources(self, url: str):
        sources = self.api.get_sources(url)
        return sources

    def search(self, query: str, mediatype: str):
        search_list = self.get_search_results(query, mediatype)
        if mediatype == g.MEDIA_MOVIE:
            self.list_builder.movie_menu_builder(search_list)
        elif mediatype == g.MEDIA_SHOW:
            self.list_builder.show_list_builder(search_list)

    def get_search_results(self, query: str, mediatype: str):
        return self.api.search(query, mediatype)