# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.request import Request


class Provider:
    def __init__(self, display_name: str, name: str, urls: list):
        self.display_name = display_name
        self.name = name
        self.urls = urls
        self.requests = Request(self.urls[0])

    def movies(self, category: str = None):
        pass

    def tv_shows(self, category: str = None):
        pass

    def resolve(self, url):
        return url

    def search(self, query, mediatype: str):
        return []