# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.provider_menu import ProviderMenu
from resources.lib.modules.globals import g

class MediaMenu(ProviderMenu):
    def __init__(self):
        super().__init__()

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
                cat['title'],
                action="movies",
                action_args={"provider": self.api.name},
                category=cat['url'],
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
                cat['title'],
                action="shows",
                action_args={"provider": self.api.name},
                category=cat['url'],
            )
        g.close_directory(g.CONTENT_FOLDER)

    def show_seasons(self, url: str):
        try:
            seasons_list = self.api.get_shows_seasons(url)
        except Exception:
            seasons_list = []
        if not seasons_list or len(seasons_list) == 1:
            return self.episodes(url)
        self.list_builder.season_list_builder(seasons_list)

    def episodes(self, url: str):
        episodes_list = self.api.get_season_episodes(url)
        self.list_builder.episode_list_builder(episodes_list)

    def search(self, query: str, mediatype: str):
        search_list = self.get_search_results(query, mediatype)
        if mediatype == g.MEDIA_MOVIE:
            self.list_builder.movie_menu_builder(search_list)
        elif mediatype == g.MEDIA_SHOW:
            self.list_builder.show_list_builder(search_list)

    def get_search_results(self, query: str, mediatype: str):
        return self.api.search(query, mediatype)
