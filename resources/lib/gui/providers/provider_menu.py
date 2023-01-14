# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.list_builder import ListBuilder


class ProviderMenu:
    def __init__(self):
        self.list_builder = ListBuilder()
        self.api = None
        self.page_limit = g.get_int_setting("item.limit")
        self.page_start = (g.PAGE - 1) * self.page_limit
        self.page_end = g.PAGE * self.page_limit

    def sources(self, url: str):
        sources = self.api.get_sources(url)
        return sources