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
            ["https://shahed4u.vip/"],
        )

    def get_movies_categories(self) -> list:
        return self._get_categories('home2/', 2)

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
        if mediatype == g.MEDIA_CHANNEL:
            return []
        type_ = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        page = self._get_paginated_page('?s={}&type={}'.format(query, type_))
        return self._get_posts(page, mediatype)

    def get_sources(self, url: str) -> list:
        return self._get_download_sources(url) + self._get_player_sources(url)

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

    def _get_download_sources(self, url: str) -> list:
        page = self._get_download_page(url)
        return self._extract_sources_meta(
            page,
            lambda soup: soup.find(class_="download-media").find_all("a"),
            quality=lambda a_tag: a_tag.find('span', class_='quality').get_text(),
            provider=lambda a_tag: a_tag.find('span', class_='name').get_text(),
            url=lambda a_tag: a_tag.get('href'),
            type=lambda a_tag: 'hoster'
        )

    def _get_player_sources(self, url: str) -> list:
        page = self.requests.get(url + 'watch/').text
        sources = self._extract_sources_meta(
            page,
            lambda soup: soup.find(class_="servers-list").find_all("li"),
            url=lambda li_tag: {"id": li_tag.get('data-id'), "i": li_tag.get('data-i'), "meta": li_tag.get('data-meta'), "type": li_tag.get("data-type")},
            type=lambda li_tag: 'hoster'
        )
        return self._get_player_source_url(page, url, sources)

    def _get_download_page(self, url: str):
        page = self.requests.get(url + 'download/').text
        import re
        ajax_url = re.search('MyAjaxURL = \"(.*)\";.*', page).group(1)
        media_id = re.search('data: {id: \"(.*)\"}.*', page).group(1)
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        page = self.requests.post(ajax_url + 'Single/Download.php', 'id=' + media_id, headers=headers).text
        return page

    def _get_player_source_url(self, page: str, url: str, sources: list) -> list:
        import re
        ajax_url = re.search('MyAjaxURL = \"(.*)\";.*', page).group(1)
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'Referer': url
        }
        for source in sources:
            iframe = self.requests.post(ajax_url + 'Single/Server.php', source['url'], headers=headers).text
            source['url'] = re.search('src="([^"]+)"', iframe).group(1)

        return sources
