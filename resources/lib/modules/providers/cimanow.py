# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.common.exceptions import try_and_log
from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.providers.provider_utils import get_quality

from bs4 import BeautifulSoup
from resources.lib.modules.providers.provider import Provider


class Cimanow(Provider):
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
        seasons = []
        response = self.requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        seasons_div = soup.find('section', {'aria-label': "seasons"}).ul.find_all('li')
        g.log('Seasons found: {}'.format(len(seasons_div)))
        if not seasons_div or len(seasons_div) == 1:
            g.log('Seasons found returning: {}'.format(len(seasons_div)))
            return seasons

        landscape = poster = clearlogo = None
        try:
            landscape = soup.find('ul', id='eps').find_all('img')[1]['src']
            poster = landscape.replace('-كوفر', '') if '-كوفر' in landscape else landscape
            clearlogo = landscape.replace('-كوفر', '-لوجو') if '-كوفر' in landscape else landscape
        except Exception:
            pass

        from collections import defaultdict
        for season_div in seasons_div:
            season = defaultdict(dict)

            season_div_a = season_div.a
            for x in season_div_a.find_all('em'): x.extract()
            season['info']['title'] = season_div_a.get_text()
            season['info']['mediatype'] = g.MEDIA_SEASON
            season['art']['poster'] = poster
            season['art']['clearlogo'] = clearlogo
            season['art']['landscape'] = landscape

            season['provider'] = self.name
            season['url'] = season_div_a.get('href').strip()

            season['args'] = g.create_args(season)
            seasons.append(season)
        return seasons

    def get_season_episodes(self, url: str):
        episodes = []
        response = self.requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        from collections import defaultdict
        for episode_div in soup.find('ul', id='eps').find_all('li'):
            episode = defaultdict(dict)

            episode_div_a = episode_div.a
            landscape_img = episode_div_a.find_all('img')[1]
            landscape = landscape_img['src']
            poster = landscape.replace('-كوفر', '') if '-كوفر' in landscape else landscape
            clearlogo = landscape.replace('-كوفر', '-لوجو') if '-كوفر' in landscape else landscape

            episode['art']['poster'] = poster
            episode['art']['clearlogo'] = clearlogo
            episode['art']['landscape'] = landscape
            episode['info']['mediatype'] = g.MEDIA_EPISODE

            episode['info']['title'] = landscape_img['alt']

            episode['url'] = episode_div_a.get('href')
            episode['provider'] = self.name

            episode['args'] = g.create_args(episode)
            episodes.append(episode)

        return episodes

    def search(self, query: str, mediatype: str):
        # type = 'series' if mediatype == g.MEDIA_SHOW else 'movie'
        return self._get_posts('?s={}'.format(query, type), mediatype)

    def get_sources(self, url: str):
        sources = []
        response = self.requests.get(url + 'watching/')
        soup = BeautifulSoup(response.text, 'html.parser')
        for source in soup.find('li', {'aria-label': 'download'}).find_all("a"):
            source = {'display_name': source.get_text(),
                      'release_title': soup.find('figure').img['alt'],
                      'url': source.get('href').strip(),
                      'quality': 'unknown',
                      'type': 'hoster',
                      'origin': self.name}
            MetadataHandler.improve_source(source)
            sources.append(source)
        return sources

    def _get_posts(self, page: str, mediatype: str) -> list:
        posts = []
        page = "{}/page/{}".format(page, g.PAGE) if g.PAGE > 1 else page
        response = self.requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')

        from collections import defaultdict
        duplicates = {}  # used mostly to filter episodes
        for postDiv in soup.find('section', {'aria-label': 'posts'}).find_all('article'):
            poster = postDiv.a.img['data-src']
            if mediatype == g.MEDIA_SHOW and duplicates.get(poster):
                continue

            post = defaultdict(dict)
            titleTag = postDiv.find('li', {'aria-label': 'title'})
            for x in titleTag.find_all('em'): x.extract()
            post['info']['title'] = titleTag.get_text()
            post['art']['poster'] = poster
            post['info']['year'] = postDiv.find('li', {'aria-label': 'year'}).next
            post['info']['mediatype'] = mediatype

            post['url'] = postDiv.a.get('href')
            post['provider'] = self.name

            post['args'] = g.create_args(post)
            posts.append(post)
            duplicates[poster] = post

        page = self._get_current_page_number(soup)
        if page:
            posts.append(page + 1)

        return posts

    def _get_categories(self, page_url) -> list:
        page = self.requests.get(page_url).text
        return self._extract_categories_meta(
            page,
            lambda soup: soup.find_all('section'),
            lambda section: section.span.next,
            lambda section: section.find('a').get('href'),
        )

    @staticmethod
    def _get_current_page_number(soup):
        pages = soup.find('ul', {'aria-label': 'page-numbers'})
        if pages:
            page = pages.select_one('li.active > a')
            if page:
                g.log('Current Page: ' + page.get_text())
                return int(page.get_text())

        return None
