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


class Shahed4uMenus(Menus):
    def __init__(self):
        super().__init__()
        self.api = Shahed4u()
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
            return self.episodes(url + 'list/')
        self.list_builder.season_list_builder(seasons_list)

    def episodes(self, url: str):
        episodes_list = self.api.get_season_episodes(url)
        self.list_builder.episode_list_builder(episodes_list)

    def sources(self, url: str):
        sources = self.api.get_sources(url)
        return sources

    def search(self, query: str, mediatype: str):
        search_list = self.api.search(query, mediatype)
        if mediatype == 'movie':
            self.list_builder.movie_menu_builder(search_list)
        elif mediatype == 'tvshow':
            self.list_builder.show_list_builder(search_list)


    # @staticmethod
    # def movies_search_history():
    #     history = SearchHistory().get_search_history("movie")
    #     g.add_directory_item(
    #         g.get_language_string(30200),
    #         action="moviesSearch",
    #         description=g.get_language_string(30399),
    #     )
    #     g.add_directory_item(
    #         g.get_language_string(30199),
    #         action="clearSearchHistory",
    #         mediatype="movie",
    #         is_folder=False,
    #         description=g.get_language_string(30409),
    #     )
    #
    #     for i in history:
    #         g.add_directory_item(i, action="moviesSearchResults", action_args=i)
    #     g.close_directory(g.CONTENT_FOLDER)
    #
    # def movies_search(self, query=None):
    #     if query is None:
    #         query = g.get_keyboard_input(heading=g.get_language_string(30013))
    #         if not query:
    #             g.cancel_directory()
    #             return
    #
    #     if g.get_bool_setting("searchHistory"):
    #         SearchHistory().add_search_history("movie", query)
    #
    #     self.movies_search_results(query)
    #
    # def movies_search_results(self, query):
    #     trakt_list = self.movies_database.extract_trakt_page(
    #         "search/movie",
    #         query=query,
    #         extended="full",
    #         page=g.PAGE,
    #         hide_watched=False,
    #         hide_unaired=False,
    #     )
    #
    #     if not trakt_list:
    #         g.cancel_directory()
    #         return
    #     self.list_builder.movie_menu_builder(
    #         [
    #             movie
    #             for movie in trakt_list
    #             if float(movie["trakt_object"]["info"]["score"]) > 0
    #         ],
    #         hide_watched=False,
    #         hide_unaired=False,
    #     )
    #
    # def movies_related(self, args):
    #     trakt_list = self.movies_database.extract_trakt_page(
    #         "movies/{}/related".format(args), page=g.PAGE, extended="full"
    #     )
    #     self.list_builder.movie_menu_builder(trakt_list)
    #
    # @staticmethod
    # def movies_years():
    #     from datetime import datetime
    #
    #     year = int(datetime.today().year)
    #     years = []
    #     for i in range(year - 100, year + 1):
    #         years.append(i)
    #     years = sorted(years, reverse=True)
    #     [
    #         g.add_directory_item(str(i), action="movieYearsMovies", action_args=i)
    #         for i in years
    #     ]
    #     g.close_directory(g.CONTENT_FOLDER)
    #
    # def movie_years_results(self, year):
    #     trakt_list = self.movies_database.extract_trakt_page(
    #         "movies/popular", years=year, page=g.PAGE, extended="full"
    #     )
    #     self.list_builder.movie_menu_builder(trakt_list)
    #
    # def movies_by_actor(self, query):
    #     if query is None:
    #         query = g.get_keyboard_input(g.get_language_string(30013))
    #         if not query:
    #             g.cancel_directory()
    #             return
    #
    #     if g.get_bool_setting("searchHistory"):
    #         SearchHistory().add_search_history("movieActor", query)
    #
    #     query = g.transliterate_string(query)
    #     # Try to deal with transliterated chinese actor names as some character -> word transliterations can be joined
    #     # I have no idea of the rules and it could well be arbitrary
    #     # This approach will only work if only one pair of adjoining transliterated chars are joined
    #     name_parts = query.split()
    #     for i in range(len(name_parts), 0, -1):
    #         query = "-".join(name_parts[:i]) + "-".join(name_parts[i:i + 1])
    #         query = tools.quote_plus(query)
    #
    #         trakt_list = self.movies_database.extract_trakt_page(
    #             "people/{}/movies".format(query),
    #             extended="full",
    #             page=g.PAGE,
    #             hide_watched=False,
    #             hide_unaired=False
    #         )
    #         if not trakt_list:
    #             continue
    #         else:
    #             break
    #
    #     try:
    #         if not trakt_list or 'trakt_id' not in trakt_list[0]:
    #             raise KeyError
    #     except KeyError:
    #         g.cancel_directory()
    #         return
    #     self.list_builder.movie_menu_builder(trakt_list,
    #                                          hide_watched=False,
    #                                          hide_unaired=False)
    #
    # def movies_genres(self):
    #     g.add_directory_item(
    #         g.get_language_string(30045), action="movieGenresGet",
    #         menu_item={
    #                 "art": dict.fromkeys(
    #                     ['icon', 'poster', 'thumb', 'fanart'], g.GENRES_PATH + "list.png"
    #                 )
    #             }
    #     )
    #     genres = self.trakt.get_json_cached("genres/movies")
    #     if genres is None:
    #         g.cancel_directory()
    #         return
    #     for i in genres:
    #         g.add_directory_item(
    #             i["name"], action="movieGenresGet", action_args=i["slug"],
    #             menu_item={
    #                 "art": dict.fromkeys(
    #                     ['icon', 'poster', 'thumb', 'fanart'], "{}{}.png".format(g.GENRES_PATH, i["slug"])
    #                 )
    #             }
    #         )
    #     g.close_directory(g.CONTENT_GENRES)
    #
    # def movies_genre_list(self, args):
    #     trakt_endpoint = (
    #         "trending"
    #         if g.get_int_setting("general.genres.endpoint") == 0
    #         else "popular"
    #     )
    #     if args is None:
    #         genre_display_list = []
    #         genres = self.trakt.get_json_cached("genres/movies")
    #         for genre in genres:
    #             gi = xbmcgui.ListItem(genre["name"])
    #             gi.setArt({"thumb": "{}{}.png".format(g.GENRES_PATH, genre["slug"])})
    #             genre_display_list.append(gi)
    #         genre_multiselect = xbmcgui.Dialog().multiselect(
    #             "{}: {}".format(g.ADDON_NAME, g.get_language_string(30326)),
    #             genre_display_list, useDetails=True
    #         )
    #         if genre_multiselect is None:
    #             return
    #         genre_string = ",".join([genres[i]["slug"] for i in genre_multiselect])
    #     else:
    #         genre_string = tools.unquote(args)
    #
    #     trakt_list = self.movies_database.extract_trakt_page(
    #         "movies/{}".format(trakt_endpoint),
    #         genres=genre_string,
    #         page=g.PAGE,
    #         extended="full"
    #     )
    #
    #     if trakt_list is None:
    #         g.cancel_directory()
    #         return
    #
    #     self.list_builder.movie_menu_builder(trakt_list, next_args=genre_string)
    #
    # @trakt_auth_guard
    # def my_watched_movies(self):
    #     watched_movies = movies.TraktSyncDatabase().get_watched_movies(g.PAGE)
    #     self.list_builder.movie_menu_builder(watched_movies)
