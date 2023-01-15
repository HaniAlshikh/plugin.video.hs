# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os

import bs4
from bs4 import BeautifulSoup

from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.providers.provider import Provider
from resources.lib.modules.providers.provider_utils import get_quality
from resources.lib.modules.request import Request


class MediaProvider(Provider):
    def __init__(self, display_name: str, name: str, urls: list):
        super().__init__(display_name, name, urls)

    def get_movies_categories(self) -> list:
        return []

    def get_movies_list(self, category: str) -> list:
        page = self._get_paginated_page(category)
        return self._get_posts(page, g.MEDIA_MOVIE)

    def get_shows_categories(self) -> list:
        return []

    def get_shows_list(self, category: str) -> list:
        page = self._get_paginated_page(category)
        return self._get_posts(page, g.MEDIA_SHOW)

    def get_shows_seasons(self, url: str) -> list:
        return []

    def get_season_episodes(self, url: str) -> list:
        return []

    def get_channels_categories(self) -> list:
        return []

    def get_channels_list(self, category: str) -> list:
        return []

    def search(self, query, mediatype: str) -> list:
        return []

    def get_sources(self, url: str) -> list:
        return []

    def sync(self):
        return

    def _get_posts(self, page: str, mediatype: str) -> list:
        return []

    def _get_paginated_page(self, url: str) -> str:
        return url
