# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.shahed4uMenus import Shahed4uMenus
from resources.lib.modules.globals import g


class Menus:
    def __init__(self):
        # self.list_builder = ListBuilder()
        self.page_limit = 20 #g.get_int_setting("item.limit")
        self.page_start = (g.PAGE - 1) * self.page_limit
        self.page_end = g.PAGE * self.page_limit
        self.PROVIDERS = {}
        self._init_providers()

    def _init_providers(self):
        self.PROVIDERS = {
            'shahed4u': Shahed4uMenus(),
        }

    ######################################################
    # MENUS
    ######################################################

    def providers(self):
        for provider in self.PROVIDERS.values():
            g.add_directory_item(
                provider.api.display_name,
                action="providerMenu",
                action_args={"provider": provider.api.name},
                description='قائمة افلام ومسلسلات موقع {}'.format(provider.api.display_name),
            )
        g.close_directory(g.CONTENT_FOLDER)

    def provider_menu(self, provider: str):
        g.add_directory_item(
            "افلام",
            action="movies".format(provider),
            action_args={"provider": provider},
            description='قائمة الافلام',
        )
        g.add_directory_item(
            "مسلسلات",
            action="shows".format(provider),
            action_args={"provider": provider},
            description='قائمة المسلسلات',
        )
        g.add_directory_item(
            "بحث",
            action="search".format(provider),
            action_args={"provider": provider},
            description='بحث شامل في الموقع',
        )
        g.close_directory(g.CONTENT_FOLDER)
