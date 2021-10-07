# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os

import bs4
from bs4 import BeautifulSoup

from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.providers.provider_utils import get_quality
from resources.lib.modules.request import Request


class Provider:
    def __init__(self, display_name: str, name: str, urls: list):
        self.display_name = display_name
        self.name = name
        self.urls = urls
        self.requests = Request(self.urls[0])

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

    def search(self, query, mediatype: str) -> list:
        return []

    def get_sources(self, url: str) -> list:
        return []

    def _get_posts(self, page: str, mediatype: str) -> list:
        return []

    def _get_current_page_number(self, soup: bs4.BeautifulSoup) -> int:
        return self._extract_current_page_number(soup)

    def _get_paginated_page(self, url: str) -> str:
        return url

    ###################################################
    # HELPERS
    ###################################################

    def _extract_categories_meta(self, page, categories_div, cat_title, cat_url):
        categories = []
        soup = BeautifulSoup(page, 'html.parser')
        for cat_tag in categories_div(soup):
            categories.append({
                'title': cat_title(cat_tag),
                'url': cat_url(cat_tag)
            })
        return categories

    def _extract_posts_meta(self, page: str, mediatype, posts_tag: callable, **params) -> list:
        posts = []
        soup = BeautifulSoup(page, 'html.parser')

        from collections import defaultdict
        duplicates = {}  # used mostly to filter episodes
        for post_tag in posts_tag(soup):
            poster = params.get('poster')(post_tag) if params.get('poster') else ''
            if mediatype == g.MEDIA_SHOW and poster and duplicates.get(poster):
                continue

            post = defaultdict(dict)
            post['info']['title'] = params.get('title')(post_tag)
            post['info']['mediatype'] = mediatype

            post['art']['poster'] = poster

            post['url'] = params.get('url')(post_tag)
            post['provider'] = self.name
            post['args'] = g.create_args(post)

            posts.append(post)
            duplicates[poster] = post

        if params.get('include_page'):
            page = self._get_current_page_number(soup)
            if page:
                posts.append(page + 1)

        return posts

    def _extract_current_page_number(self, soup, **params):
        pages_tag = params.get('pages_tag')
        pages_tag = pages_tag(soup) if pages_tag else soup.find('ul', class_='page-numbers')
        if not pages_tag:
            return -1

        page_num = pages_tag.select_one('li.active > a')
        if page_num:
            return int(page_num.get_text())

        page_num = pages_tag.select_one('span.current')
        if page_num:
            return int(page_num.get_text())

        if params.get('selectors'):
            for selector in params.get('selectors'):
                page_num = selector(pages_tag)
                if page_num:
                    g.log('Current Page: ' + page_num.get_text())
                    return int(page_num.get_text())
        return -1

    def _extract_sources_meta(self, page: str, sources_tag: callable, **params) -> list:
        sources = []

        soup = BeautifulSoup(page, 'html.parser')
        for source_tag in sources_tag(soup):
            quality = get_quality(params.get('quality')(source_tag))
            provider = params.get('provider')(source_tag)
            source = {
              'display_name': provider + ' ' + quality,
              'release_title': params.get('release_title')(soup),
              'url': params.get('url')(source_tag),
              'quality': quality,
              'type': params.get('type'),
              'provider': provider,
              'origin': self.name
            }

            MetadataHandler.improve_source(source)
            sources.append(source)

        return sources

    @staticmethod
    def _generate_game_art(
            first_img: str, first_img_title: str, second_img: str, second_img_title: str, banner=False
    ) -> str:
        first_img_title = '_'.join(first_img_title.split())
        second_img_title = '_'.join(second_img_title.split())

        extension = '_banner.png' if banner else '.png'
        poster_path = os.path.join(g.TMP_PATH, first_img_title + 'vs' + second_img_title + extension)
        poster_path_reversed = os.path.join(g.TMP_PATH, second_img_title + 'vs' + first_img_title + extension)
        if not os.path.exists(poster_path):
            if os.path.exists(poster_path_reversed):
                return poster_path_reversed
            from resources.lib.common.image_generator import combine_vs
            poster = combine_vs(first_img, second_img, banner)
            poster.save(poster_path, format='png')

        return poster_path
