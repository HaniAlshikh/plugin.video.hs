# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re
from typing import TYPE_CHECKING

import bs4

from resources.lib.common.exceptions import try_and_log
from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.providers.provider_utils import get_quality

from bs4 import BeautifulSoup
from resources.lib.modules.providers.provider import Provider

import os
import sys


class Arabseed(Provider):
    def __init__(self):
        super().__init__(
            'عرب سيد',
            "arabseed",
            ["https://arabseed.onl/"],
        )

    def get_movies_categories(self):
        return self._get_categories('main/', 2)

    def get_shows_categories(self):
        return self._get_categories('main/', 4)

    def get_shows_seasons(self, url: str):
        return []

    def get_season_episodes(self, url: str):
        posts = []
        response = self.requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        from collections import defaultdict
        for postDiv in soup.select_one('div.ContainerEpisodesList').find_all('a'):
            post = defaultdict(dict)

            post['info']['title'] = postDiv.get_text()
            post['art']['poster'] = soup.select_one('div.Poster').find('img').get('src')
            post['info']['mediatype'] = g.MEDIA_EPISODE

            post['url'] = postDiv.get('href')
            post['provider'] = self.name

            post['args'] = g.create_args(post)
            posts.append(post)
        return posts

    def search(self, query: str, mediatype: str):
        type = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        response = self.requests.post(
            'wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php',
            {'search': query, 'type': type}
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._get_posts('', mediatype, soup)

    def get_sources(self, url: str):
        sources = []
        response = self.requests.get(url + 'download/')
        soup = BeautifulSoup(response.text, 'html.parser')
        for source in soup.find('div', class_="DownloadArea").find_all("a", class_='downloadsLink'):
            quality = get_quality(source.p.get_text())
            provider = source.span.get_text()
            source = {'display_name': provider + ' ' + quality,
                      'release_title': soup.find('title').get_text(),
                      'url': source.get('href').strip(),
                      'quality': quality,
                      'type': 'hoster',
                      'provider': provider,
                      'origin': self.name}
            MetadataHandler.improve_source(source)
            sources.append(source)
        return sources

    def _get_posts(self, page: str, mediatype: str, soup: bs4.BeautifulSoup = None) -> list:
        posts = []
        page = "{}/?page={}".format(page, g.PAGE) if g.PAGE > 1 else page
        if not soup:
            response = self.requests.get(page)
            soup = BeautifulSoup(response.text, 'html.parser')

        from collections import defaultdict
        duplicates = {}  # used mostly to filter episodes
        for postDiv in soup.select_one('ul.Blocks-UL').find_all('a'):
            poster_img_tag = postDiv.find('img')
            poster = poster_img_tag.get(
                next((k for k in ['data-src', 'data-image', 'src'] if poster_img_tag.get(k)), None))
            if mediatype == g.MEDIA_SHOW and duplicates.get(poster):
                continue

            post = defaultdict(dict)

            post['info']['title'] = postDiv.find('h4').get_text()
            post['art']['poster'] = poster
            post['info']['plot'] = postDiv.select_one('div.Story').get_text()
            post['info']['mediatype'] = mediatype

            post['url'] = postDiv.get('href')
            post['provider'] = self.name

            if mediatype == g.MEDIA_SHOW:
                self._improve_show_meta(post)

            post['args'] = g.create_args(post)
            posts.append(post)
            duplicates[poster] = post

        page = self._get_current_page_number(soup)
        if page:
            posts.append(page + 1)

        return posts

    def _improve_show_meta(self, show):
        show['info']['title'] = show['info']['title'].split('الحلقة')[0]
        show['info']['plot'] = '' # it's not really useful here

    def _get_categories(self, page_url, parent_cat_num: int) -> list:
        page = self.requests.get(page_url).text
        return self._extract_categories_meta(
            page,
            lambda soup: soup.select_one('ul#main-menu').find_all('li', recursive=False)[parent_cat_num].ul.find_all('a'),
            lambda a_tag: a_tag.get_text(),
            lambda a_tag: a_tag.get('href'),
        )

    def _get_current_page_number(self, soup: bs4.BeautifulSoup) -> int:
        pages = soup.find('ul', class_='page-numbers')
        if pages:
            page = pages.select_one('li.active > a')
            if not page:
                page = pages.select_one('span.current')
            if page:
                g.log('Current Page: ' + page.get_text())
                return int(page.get_text())

        return -1
