# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.providers.media.media_provider import MediaProvider
from resources.lib.modules.providers.provider_utils import get_img_src


class Arabseed(MediaProvider):
    def __init__(self):
        super().__init__(
            'عرب سيد',
            "arabseed",
            ["https://arabseed.onl/"],
        )

    def get_movies_categories(self) -> list:
        return self._get_categories('main/', 2)

    def get_shows_categories(self) -> list:
        return self._get_categories('main/', 4)

    def get_season_episodes(self, url: str) -> list:
        page = self.requests.get(url).text
        return self._extract_posts_meta(
            page, g.MEDIA_EPISODE,
            lambda soup: soup.select_one('div.ContainerEpisodesList').find_all('a'),
            title=lambda post_tag: post_tag.get_text(),
            poster=lambda post_tag: get_img_src(
                next((t.select_one('div.Poster') for t in post_tag.parentGenerator() if t.select_one('div.Poster')),
                     None).find('img')),
            url=lambda post_tag: post_tag.get('href'),
        )

    def search(self, query: str, mediatype: str):
        type_ = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        page = self.requests.post(
            'wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php',
            {'search': query, 'type': type_}
        ).text
        return self._get_posts(page, mediatype)

    def get_sources(self, url: str):
        page = self.requests.get(url + 'download/').text
        return self._extract_sources_meta(
            page,
            lambda soup: soup.find('div', class_="DownloadArea").find_all("a", class_='downloadsLink'),
            quality=lambda a_tag: a_tag.p.get_text(),
            provider=lambda a_tag: a_tag.span.get_text(),
            url=lambda a_tag: a_tag.get('href'),
            type=lambda a_tag: 'hoster'
        )

    ###################################################
    # HELPERS
    ###################################################

    def _get_categories(self, page_url, parent_cat_num: int) -> list:
        page = self.requests.get(page_url).text
        return self._extract_categories_meta(
            page,
            lambda soup: soup.select_one('ul#main-menu').find_all('li', recursive=False)[parent_cat_num].ul.find_all('a'),
            lambda a_tag: a_tag.get_text(),
            lambda a_tag: a_tag.get('href'),
        )

    def _get_paginated_page(self, url: str) -> str:
        url = "{}/?page={}".format(url, g.PAGE) if g.PAGE > 1 else url
        return self.requests.get(url).text

    def _get_posts(self, page: str, mediatype: str) -> list:
        return self._extract_posts_meta(
            page, mediatype,
            lambda soup: soup.select_one('ul.Blocks-UL').find_all('a'),
            title=lambda post_tag: post_tag.find('h4').get_text(),
            poster=lambda post_tag: get_img_src(post_tag.find('img')),
            plot=lambda post_tag: post_tag.select_one('div.Story').get_text(),
            url=lambda post_tag: post_tag.get('href'),
            edit_meta=self._improve_show_meta,
            include_page=True
        )

    def _improve_show_meta(self, show):
        if not show['info']['mediatype'] == g.MEDIA_SHOW:
            return
        show['info']['title'] = show['info']['title'].split('الحلقة')[0]
        show['info']['plot'] = '' # it's not really useful here
        show['args'] = g.create_args(show)
