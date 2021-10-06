# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.providers.provider_utils import get_img_src

from bs4 import BeautifulSoup
from resources.lib.modules.providers.provider import Provider


class Shahed4u(Provider):
    def __init__(self):
        super().__init__(
            'شاهد فور يو',
            "shahed4u",
            ["https://shahed4u.land/"],
        )

    def get_movies_categories(self):
        return self._get_categories('home5/', 2)

    def get_shows_categories(self):
        missing_categories = [{'title': 'مسلسلات عربي', 'url': '{}categorie/مسلسلات عربي'.format(self.requests.base)}]
        categories = self._get_categories('home5/', 3)
        categories.extend(missing_categories)
        return categories

    def get_shows_seasons(self, url: str):
        page = self.requests.get(url).text
        return self._extract_posts_meta(
            page, g.MEDIA_SEASON,
            lambda soup: soup.select_one("div#seasons").find_all('div', class_="content-box"),
            title=lambda season_div: season_div.find('h3').get_text(),
            poster=lambda season_div: get_img_src(season_div.find('a', class_="image").find('img')),
            url=lambda season_div: season_div.find('a', class_="image").get('href'),
        )

    def get_season_episodes(self, url: str):
        url = url + 'list/' if 'list/' not in url else url
        return self._get_posts(url, g.MEDIA_EPISODE)

    def search(self, query: str, mediatype: str):
        type_ = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        return self._get_posts('?s={}&type={}'.format(query, type_), mediatype)

    def get_sources(self, url: str):
        page = self.requests.get(url + 'download/').text
        return self._extract_sources_meta(
            page,
            lambda soup: soup.find(class_="download-media").find_all("a"),
            release_title=lambda soup: soup.find('h1').get_text(),
            quality=lambda a_tag: a_tag.find('span', class_='quality').get_text(),
            provider=lambda a_tag: a_tag.find('span', class_='name').get_text(),
            url=lambda a_tag: a_tag.get('href').strip(),
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

    def _get_posts(self, url: str, mediatype: str) -> list:
        url_pattern = "{}/?page={}" if url.endswith('list/') else "{}/page/{}"
        url = url_pattern.format(url, g.PAGE) if g.PAGE > 1 else url
        page = self.requests.get(url).text

        posts = self._extract_posts_meta(
            page, mediatype,
            lambda soup: soup.find_all('div', class_="content-box"),
            title=lambda post_tag: post_tag.a.get('title'),
            poster=lambda post_tag: get_img_src(post_tag.find('a', class_="image").find('img')),
            url=lambda post_tag: post_tag.a.get('href'),
            include_page=True
        )

        for post in posts:
            if isinstance(post, dict) and post['info']['mediatype'] == g.MEDIA_SHOW:
                self._improve_show_meta(post)

        return posts

    def _improve_show_meta(self, show):
        page = self.requests.get(show['url']).text
        soup = BeautifulSoup(page, 'html.parser')
        show_breadcrumb = soup.select_one("div.breadcrumb > a:nth-child(3)")
        show['info']['title'] = show_breadcrumb.get_text()
        show['url'] = show_breadcrumb.get('href')
        show['args'] = g.create_args(show)

    def _get_current_page_number(self, soup):
        return self._extract_current_page_number(
            soup,
            selectors=[
                lambda pages_tag: pages_tag.select_one('span.current')
            ]
        )
