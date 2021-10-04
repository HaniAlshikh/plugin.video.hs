# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.shahed4uMenus import Shahed4uMenus
from resources.lib.gui.providers.yallalive_menus import YallaliveMenus
from resources.lib.modules.globals import g
from resources.lib.modules.list_builder import ListBuilder


class ProviderMenus:
    def __init__(self):
        self.list_builder = ListBuilder()
        self.page_limit = 20 #g.get_int_setting("item.limit")
        self.page_start = (g.PAGE - 1) * self.page_limit
        self.page_end = g.PAGE * self.page_limit
        self._init_providers()

    def _init_providers(self):
        self.providers_media = {
            'shahed4u': Shahed4uMenus(),
        }
        self.providers_sports = {
            'yallalive': YallaliveMenus(),
        }

        self.PROVIDERS = {**self.providers_media, **self.providers_sports}

    ######################################################
    # MENUS
    ######################################################

    def media_providers(self):
        for provider in self.providers_media.values():
            g.add_directory_item(
                provider.api.display_name,
                action="mediaProviderMenu",
                action_args={"provider": provider.api.name},
                description='قائمة افلام ومسلسلات موقع {}'.format(provider.api.display_name),
            )
        g.close_directory(g.CONTENT_FOLDER)

    def sports_providers(self):
        for provider in self.providers_sports.values():
            g.add_directory_item(
                provider.api.display_name,
                action="games",
                action_args={"provider": provider.api.name},
                description='المباريات المنقولة من موقع {}'.format(provider.api.display_name),
            )
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def media_provider_menu(provider: str):
        g.add_directory_item(
            "افلام",
            action="movies",
            action_args={"provider": provider},
            description='قائمة الافلام',
        )
        g.add_directory_item(
            "مسلسلات",
            action="shows",
            action_args={"provider": provider},
            description='قائمة المسلسلات',
        )
        g.add_directory_item(
            "بحث",
            action="search",
            action_args={"provider": provider},
            description='بحث شامل في الموقع',
        )
        g.close_directory(g.CONTENT_FOLDER)

    def search(self, mediatype, query=None):
        if query is None:
            query = g.get_keyboard_input(heading=g.get_language_string(30013))
            if not query:
                g.cancel_directory()
                return

        # if g.get_bool_setting("searchHistory"):
        #     SearchHistory().add_search_history("movie", query)

        self.search_results(mediatype, query)

    def search_results(self, mediatype, query):
        results = []
        for p in self.PROVIDERS.values():
            provider_results = p.get_search_results(query, mediatype)
            for r in provider_results:
                r['info']['title'] = p.api.name.upper() + ': ' + r['info']['title']

            results.extend(provider_results)

        if not results:
            g.cancel_directory()
            return

        menu_builder = self.list_builder.movie_menu_builder \
            if mediatype == g.MEDIA_MOVIE else self.list_builder.show_list_builder
        menu_builder(
            results,
            hide_watched=False,
            hide_unaired=False,
        )