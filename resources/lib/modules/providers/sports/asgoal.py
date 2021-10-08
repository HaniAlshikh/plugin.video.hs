# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from bs4 import BeautifulSoup

from resources.lib.modules.globals import g

from resources.lib.modules.providers.sports.sports_provider import SportsProvider


class Asgoal(SportsProvider):
    def __init__(self):
        super().__init__(
            'اس جول',
            "asgoal",
            ["https://www.as-goal.com/"],
        )

    def get_games_list(self) -> list:
        page = self.requests.get('m/').text

        def get_title(game_div):
            playing_time = game_div.select_one('div.AlbaTableTime').get_text()

            return self._generate_title(
                game_div.find('div', class_='AlbaTableFteam').get_text(),
                game_div.find('div', class_='AlbaTableSteam').get_text(),
                playing_time
            )

        def get_poster(game_div):
            try:
                return self._generate_game_art(
                    game_div.find('div', class_='AlbaTableFteam').img['src'],
                    game_div.find('div', class_='AlbaTableFteam').get_text(),
                    game_div.find('div', class_='AlbaTableSteam').img['src'],
                    game_div.find('div', class_='AlbaTableSteam').get_text(),
                    banner=True
                )
            except Exception:
                return ''

        return self._extract_posts_meta(
            page, g.MEDIA_MOVIE,
            lambda soup: soup.find('div', id="Today").select('a.AlbaSposrTable'),
            title=get_title,
            poster=get_poster,
            url=lambda post_tag: post_tag.get('href'),
            edit_meta=self._improve_game_meta,
        )

    def get_sources(self, url: str):
        def get_url(source_div):
            channel_link = re.search('.*setURL\(\'(.*)\'\).*', source_div.get('onclick')).group(1)
            response = self.requests.get(channel_link, headers={'Referer': '/'.join(url.split('/')[:3])})
            channel_soup = BeautifulSoup(response.text, 'html.parser')
            iframe = channel_soup.find('iframe')
            if iframe:
                return iframe.get('src').strip()
            return ''

        page = self.requests.get(url).text
        return self._extract_sources_meta(
            page,
            lambda soup: soup.find(class_="servers-name").find_all("button"),
            # release_title=lambda soup: soup.find('h1').get_text(),
            quality=lambda a_tag: 'livestream',
            url=get_url,
            type=lambda a_tag: 'livestream'
        )