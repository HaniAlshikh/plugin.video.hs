# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from bs4 import BeautifulSoup

from resources.lib.modules.globals import g
from resources.lib.modules.providers.media.media_provider import MediaProvider
from resources.lib.modules.providers.provider_utils import get_img_src

class Cimanow(MediaProvider):
    def __init__(self):
        super().__init__(
            'سيما ناو',
            "cimanow",
            ["https://cimanow.cc/"],
        )

    def get_movies_categories(self):
        return self._get_categories('category/الافلام/')

    def get_shows_categories(self):
        return self._get_categories('category/المسلسلات/')

    def get_shows_seasons(self, url: str):
        page = self.requests.get(url).text
        return self._extract_posts_meta(
            page, g.MEDIA_SEASON,
            lambda soup: soup.find('section', {'aria-label': "seasons"}).ul.find_all('li'),
            title=lambda season_div: season_div.a.find(text=True),
            poster=lambda season_div: get_img_src(
                next((t.find('ul', id='eps') for t in season_div.parentGenerator() if t.find('ul', id='eps')),
                     season_div).find_all('img')[1]),
            url=lambda season_div: season_div.a.get('href'),
            edit_meta=self._improve_art_from_landscape
        )

    def get_season_episodes(self, url: str):
        page = self.requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        posts_div = lambda soup: soup.find('ul', id='eps').find_all('li')
        try:
            posts_div(soup)
        except Exception:
            url = soup.find('section', {'aria-label': "seasons"}).select_one('li.active').a.get('href')
            page = self.requests.get(url).text

        return self._extract_posts_meta(
            page, g.MEDIA_EPISODE,
            posts_div,
            title=lambda post_tag: post_tag.a.find_all('img')[1]['alt'],
            poster=lambda post_tag: get_img_src(post_tag.a.find_all('img')[1]),
            url=lambda post_tag: post_tag.a.get('href'),
            edit_meta=self._improve_art_from_landscape
        )

    def search(self, query: str, mediatype: str):
        # type = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        page = self._get_paginated_page('?s={}'.format(query))
        return self._get_posts(page, mediatype)

    def get_sources(self, url: str):
        page = self.requests.get(url + 'watching/').text
        return self._extract_sources_meta(
            page,
            lambda soup: soup.find('li', {'aria-label': 'download'}).find_all("a"),
            release_title=lambda a_tag: next((t.find('figure') for t in a_tag.parentGenerator() if t.find('figure')),
                     a_tag).img['alt'],
            quality=lambda a_tag: 'Unknown',
            provider=lambda a_tag: a_tag.get_text(),
            url=lambda a_tag: a_tag.get('href'),
            type=lambda a_tag: 'hoster'
        )

    ###################################################
    # HELPERS
    ###################################################

    def _get_categories(self, page_url) -> list:
        page = self.requests.get(page_url).text
        return self._extract_categories_meta(
            page,
            lambda soup: soup.find_all('section'),
            lambda section: section.span.next,
            lambda section: section.find('a').get('href'),
        )

    def _get_paginated_page(self, url: str) -> str:
        url = "{}page/{}".format(url, g.PAGE) if g.PAGE > 1 else url
        return self.requests.get(url).text

    def _get_posts(self, page: str, mediatype: str) -> list:
        return self._extract_posts_meta(
            page, mediatype,
            lambda soup: soup.find('section', {'aria-label': 'posts'}).find_all('article'),
            title=lambda post_tag: ' '.join(post_tag.find('li', {'aria-label': 'title'}).find_all(text=True, recursive=False)),
            poster=lambda post_tag: get_img_src(post_tag.a.img),
            year=lambda post_tag: post_tag.find('li', {'aria-label': 'year'}).next,
            url=lambda post_tag: post_tag.a.get('href'),
            include_page=True
        )

    def _improve_art_from_landscape(self, season: dict):
        if not season.get('landscape'):
            return
        landscape = season['landscape']
        season['poster'] = landscape.replace('-كوفر', '') if '-كوفر' in landscape else landscape
        season['clearlogo'] = landscape.replace('-كوفر', '-لوجو') if '-كوفر' in landscape else landscape

    def _get_current_page_number(self, soup) -> int:
        return self._extract_current_page_number(
            soup,
            pages_tag=lambda soup: soup.find('ul', {'aria-label': 'pagination'})
        )