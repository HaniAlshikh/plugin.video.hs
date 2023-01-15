# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.media.arabseed_menu import ArabseedMenu
from resources.lib.gui.providers.media.magichd_menu import MagicHDMenu
from resources.lib.gui.providers.sports.alostora_menu import AlostoraMenu
from resources.lib.gui.providers.sports.asgoal_menu import AsgoalMenu
from resources.lib.gui.providers.media.cimanow_menu import CimanowMenu
from resources.lib.gui.providers.media.shahed4u_menu import Shahed4uMenu
from resources.lib.gui.providers.sports.yallalive_menus import YallaliveMenu
from resources.lib.modules.globals import g
from resources.lib.modules.list_builder import ListBuilder


class ProviderMenus:
    def __init__(self):
        self.list_builder = ListBuilder()
        self._init_providers()

    def _init_providers(self):
        self.providers_media = {
            'arabseed': ArabseedMenu(),
            'shahed4u': Shahed4uMenu(),
            'cimanow': CimanowMenu(),
            'magichd': MagicHDMenu(),
        }
        self.providers_sports = {
            'alostora': AlostoraMenu(),
            'asgoal': AsgoalMenu(),
            'yallalive': YallaliveMenu(),
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

    def media_provider_menu(self, provider: str):
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
        if self.PROVIDERS[provider].api.support_channels:
            g.add_directory_item(
                "قنوات",
                action="channels",
                action_args={"provider": provider},
                description='قائمة القنوات',
            )
        g.add_directory_item(
            "بحث",
            action="search",
            action_args={"provider": provider},
            description='بحث شامل في الموقع',
        )
        g.close_directory(g.CONTENT_FOLDER)

    def search(self, query=None, mediatype=None, provider=None):
        if provider:
            if not mediatype:
                mediatypes = {'فلم': g.MEDIA_MOVIE, 'مسلسل': g.MEDIA_SHOW}
                if provider and self.PROVIDERS[provider].api.support_channels:
                    mediatypes['قناة'] = g.MEDIA_CHANNEL
                mediatype = g.get_option_input('بحث عن', mediatypes)
                if not mediatype:
                    return

        if query is None:
            query = g.get_keyboard_input(heading=g.get_language_string(30013))
            if not query:
                g.cancel_directory()
                return

        if provider:
            return self.PROVIDERS[provider].search(query, mediatype)

        # if g.get_bool_setting("searchHistory"):
        #     SearchHistory().add_search_history("movie", query)

        g.show_busy_dialog()
        self.global_search_results(mediatype, query)
        g.close_busy_dialog()

    def global_search_results(self, mediatype, query):
        results = []
        for p in self.providers_media.values():
            try:
                provider_results = p.get_search_results(query, mediatype)
                for r in provider_results:
                    r['info']['title'] = p.api.name.upper() + ': ' + r['info']['title']

                results.extend(provider_results)
            except:
                g.log('failed searching {}|{} for {}'.format(p.api.name, mediatype, query))

        if not results:
            g.cancel_directory()
            return []

        menu_builder = self.list_builder.movie_menu_builder \
            if mediatype == g.MEDIA_MOVIE else self.list_builder.show_list_builder
        menu_builder(
            results,
            hide_watched=False,
            hide_unaired=False,
            no_paging=True
        )