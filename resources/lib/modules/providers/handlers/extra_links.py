# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.request import Request


class ExtraLinks:

    def __init__(self):
        self.source = g.get_setting('general.customLinks')
        self.request = Request(self.source)

    def get_links(self):
        g.PAGE = -1
        links = self.request.get().json()
        for link in links:
            link['args'] = g.create_args(link)
        return links
