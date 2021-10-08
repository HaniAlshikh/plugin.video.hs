# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from bs4 import BeautifulSoup

from resources.lib.modules.globals import g

from resources.lib.modules.providers.sports.sports_provider import SportsProvider


class Alostora(SportsProvider):
    def __init__(self):
        super().__init__(
            'الاسطورة',
            "alostora",
            ["https://livehd7.live/"],
        )

    def get_games_list(self) -> list:
        page = self.requests.get().text

        def get_title(game_div):
            return self._generate_title(
                game_div.find('div', class_='team-first').find('div', {'class': re.compile(".*team_title")}).get_text(),
                game_div.find('div', class_='team-second').find('div', {'class': re.compile(".*team_title")}).get_text(),
                game_div.find('div', {'class': 'matchTime'}).get_text()
            )

        def get_poster(game_div):
            try:
                return self._generate_game_art(
                    game_div.find('div', class_='team-first').find('img').get('src'),
                    game_div.find('div', class_='team-first').find('div', {'class': re.compile(".*team_title")}).get_text(),
                    game_div.find('div', class_='team-second').find('img').get('src'),
                    game_div.find('div', class_='team-second').find('div', {'class': re.compile(".*team_title")}).get_text(),
                    banner=True
                )
            except Exception:
                return ''

        return self._extract_posts_meta(
            page, g.MEDIA_MOVIE,
            lambda soup: soup.find('div', id="today").div,
            title=get_title,
            poster=get_poster,
            url=lambda post_tag: post_tag.a.get('href'),
            edit_meta=self._improve_game_meta,
        )

    def get_sources(self, url: str):
        def get_sources(soup):
            sources = []
            for iframe in soup.find_all('iframe'):
                page = self.requests.get(iframe.get('src'), headers={'Referer': '/'.join(url.split('/')[:3])}).text
                soup = BeautifulSoup(page, 'html.parser')
                sources.extend(soup.find(class_="albaplayer_name").find_all("a"))
            return sources

        def get_url(source_div):
            channel_link = source_div.get('href')
            response = self.requests.get(channel_link, headers={'Referer': '/'.join(url.split('/')[:3])})
            channel_soup = BeautifulSoup(response.text, 'html.parser')
            player = channel_soup.select_one('div#player')
            if player:
                script = player.next_sibling
                g.log('script: ' + str(script.string))
                encoded_link = re.search('AlbaPlayerControl\(\'(.*)\'.*', script.string).group(1)
                import base64
                return base64.b64decode(encoded_link).decode('utf-8')
            iframe = channel_soup.find('iframe')
            if iframe:
                return iframe.get('src').strip()
            return ''

        page = self.requests.get(url).text
        return self._extract_sources_meta(
            page,
            get_sources,
            provider=lambda source_div: source_div.get_text(),
            # release_title=lambda soup: soup.find('h1').get_text(),
            quality=lambda a_tag: 'livestream',
            url=get_url,
            type=lambda a_tag: 'livestream'
        )