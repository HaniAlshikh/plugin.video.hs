# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.providers.media.media_provider import MediaProvider
from resources.lib.modules.providers.provider_utils import get_img_src

from bs4 import BeautifulSoup


class Shahed4u(MediaProvider):
    def __init__(self):
        super().__init__(
            'شاهد فور يو',
            "shahed4u",
            ["https://shahed4u.land/"],
        )

    def get_movies_categories(self) -> list:
        return self._get_categories('home5/', 2)

    def get_shows_categories(self) -> list:
        missing_categories = [{'title': 'مسلسلات عربي', 'url': '{}category/مسلسلات-عربي/'.format(self.requests.base)}]
        categories = self._get_categories('home5/', 3)
        categories.extend(missing_categories)
        return categories

    def get_shows_seasons(self, url: str) -> list:
        page = self.requests.get(url).text
        return self._extract_posts_meta(
            page, g.MEDIA_SEASON,
            lambda soup: soup.select_one("div#seasons").find_all('div', class_="content-box"),
            title=lambda season_div: season_div.find('h3').get_text(),
            poster=lambda season_div: get_img_src(season_div.find('a', class_="image").find('img')),
            url=lambda season_div: season_div.find('a', class_="image").get('href'),
        )

    def get_season_episodes(self, url: str) -> list:
        url = url + 'list/' if 'list/' not in url else url
        page = self._get_paginated_page(url)
        return self._get_posts(page, g.MEDIA_EPISODE)

    def search(self, query: str, mediatype: str) -> list:
        type_ = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        page = self._get_paginated_page('?s={}&type={}'.format(query, type_))
        return self._get_posts(page, mediatype)

    def get_sources(self, url: str) -> list:
        page = self.requests.get(url + 'download/').text
        return self._extract_sources_meta(
            page,
            lambda soup: soup.find(class_="download-media").find_all("a"),
            release_title=lambda soup: soup.find('h1').get_text(),
            quality=lambda a_tag: a_tag.find('span', class_='quality').get_text(),
            provider=lambda a_tag: a_tag.find('span', class_='name').get_text(),
            url=lambda a_tag: a_tag.get('href'),
            type='hoster'
        )

    ###################################################
    # HELPERS
    ###################################################

    def _get_categories(self, page_url, parent_cat_num: int) -> list:
        page = self.requests.get(page_url).text
        return self._extract_categories_meta(
            page,
            lambda soup: soup.select_one("ul#main_nav_header > li:nth-child({})".format(parent_cat_num)).find_all('a'),
            lambda a_tag: a_tag.get_text(),
            lambda a_tag: a_tag.get('href'),
        )

    def _get_paginated_page(self, url: str) -> str:
        page_pattern = "?page={}" if url.endswith('list/') else "page/{}"
        page_part = page_pattern.format(g.PAGE) if g.PAGE > 1 else ''
        url = '{}{}'.format(page_part, url) if url.startswith('?s') else '{}{}'.format(url, page_part)
        return self.requests.get(url).text

    def _get_posts(self, page: str, mediatype: str) -> list:
        return self._extract_posts_meta(
            page, mediatype,
            lambda soup: soup.find_all('div', class_="content-box"),
            title=lambda post_tag: post_tag.a.get('title'),
            poster=lambda post_tag: get_img_src(post_tag.find('a', class_="image").find('img')),
            url=lambda post_tag: post_tag.a.get('href'),
            edit_meta=self._improve_show_meta,
            include_page=True
        )

    def _improve_show_meta(self, show):
        if not show['info']['mediatype'] == g.MEDIA_SHOW:
            return
        page = self.requests.get(show['url']).text
        soup = BeautifulSoup(page, 'html.parser')
        show_breadcrumb = soup.select_one("div.breadcrumb > a:nth-child(3)")
        show['info']['title'] = show_breadcrumb.get_text()
        show['url'] = show_breadcrumb.get('href')
        show['args'] = g.create_args(show)
