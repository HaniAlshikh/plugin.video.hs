# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g


class Menus:
    def __init__(self):
        # self.list_builder = ListBuilder()
        self.page_limit = 20 #g.get_int_setting("item.limit")
        self.page_start = (g.PAGE - 1) * self.page_limit
        self.page_end = g.PAGE * self.page_limit

    ######################################################
    # MENUS
    ######################################################

    def movies(self, category: str = ""):
        pass

    def tv_shows(self, category: str = ""):
        pass

    def search(self, query: str, section: str):
        pass
