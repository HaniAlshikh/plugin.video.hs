# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re
from typing import TYPE_CHECKING

from resources.lib.common.exceptions import try_and_log
from resources.lib.common.tools import get_any
from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.providers.provider_utils import get_quality, get_img_src

from bs4 import BeautifulSoup
from resources.lib.modules.providers.provider import Provider

import os
import sys


class Shahed4u(Provider):
    def __init__(self):
        super().__init__(
            'شاهد فور يو',
            "shahed4u",
            ["https://shahed4u.land/"],
        )

    def get_movies_categories(self):
        return self._get_categories('home5/', 2)

    def get_movies_list(self, category: str):
        return self._get_posts(category, g.MEDIA_MOVIE)

    def get_shows_categories(self):
        missing_categories = [{'title': 'مسلسلات عربي', 'url': '{}categorie/مسلسلات عربي'.format(self.requests.base)}]
        categories = self._get_categories('home5/', 3)
        categories.extend(missing_categories)
        return categories

    def get_shows_list(self, category: str):
        return self._get_posts('category/' + category, g.MEDIA_SHOW)

    @try_and_log()
    def get_shows_seasons(self, url: str):
        seasons = []
        response = self.requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        seasons_div = soup.select_one("div#seasons")
        if not seasons_div:
            return seasons

        from collections import defaultdict
        for season_div in seasons_div.find_all('div', class_="content-box"):
            season = defaultdict(dict)

            img_a = season_div.find('a', class_="image")
            season['info']['title'] = season_div.find('h3').get_text()
            season['info']['mediatype'] = g.MEDIA_SEASON
            season['art']['poster'] = img_a.img.get('data-image')

            season['provider'] = self.name
            season['url'] = img_a.get('href')

            season['args'] = g.create_args(season)
            seasons.append(season)
        return seasons

    def get_season_episodes(self, url: str):
        url = url + 'list/' if 'list/' not in url else url
        return self._get_posts(url, g.MEDIA_EPISODE)

    def search(self, query: str, mediatype: str):
        type = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        return self._get_posts('?s={}&type={}'.format(query, type), mediatype)

    @try_and_log()
    def get_sources(self, url: str):
        sources = []
        response = self.requests.get(url + 'download/')
        soup = BeautifulSoup(response.text, 'html.parser')
        for source in soup.find(class_="download-media").find_all("a"):
            quality = get_quality(source.find('span', class_='quality').get_text())
            provider = source.find('span', class_='name').get_text()
            source = {'display_name': provider + ' ' + quality,
                      'release_title': soup.find('h1').get_text(),
                      'url': source.get('href').strip(),
                      'quality': quality,
                      'type': 'hoster',
                      'provider': provider,
                      'origin': self.name}
            MetadataHandler.improve_source(source)
            sources.append(source)
        return sources

    def _get_posts(self, page: str, mediatype: str) -> list:
        url_pattern = "{}/?page={}" if page.endswith('list/') else "{}/page/{}"
        page = url_pattern.format(page, g.PAGE) if g.PAGE > 1 else page
        response = self.requests.get(page)

        posts = self._extract_post_meta(
            response.text, mediatype,
            lambda soup: soup.find_all('div', class_="content-box"),
            poster=lambda post_tag: get_img_src(post_tag.find('a', class_="image").find('img')),
            title=lambda post_tag: post_tag.a.get('title'),
            url=lambda post_tag: post_tag.a.get('href'),
            provider=self.name,
            include_page=True
        )

        for post in posts:
            if isinstance(post, dict) and post['info']['mediatype'] == g.MEDIA_SHOW:
                self._improve_show_meta(post)

        return posts

    def _improve_show_meta(self, show):
        response = self.requests.get(show['url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        show_breadcrumb = soup.select_one("div.breadcrumb > a:nth-child(3)")
        show['info']['title'] = show_breadcrumb.get_text()
        show['url'] = show_breadcrumb.get('href')
        show['args'] = g.create_args(show)

    def _get_categories(self, page, number: int) -> list:
        response = self.requests.get(page)
        return self._extract_categories_meta(
            response.text,
            lambda soup: soup.select_one("ul#main_nav_header > li:nth-child({})".format(number)).find_all('a'),
            lambda a_tag: a_tag.get_text(),
            lambda a_tag: a_tag.get('href'),
        )

    def _get_current_page_number(self, soup):
        pages = soup.find('ul', class_='page-numbers')
        if pages:
            page = pages.select_one('li.active > a')
            if not page:
                page = pages.select_one('span.current')
            if page:
                g.log('Current Page: ' + page.get_text())
                return int(page.get_text())

        return None
