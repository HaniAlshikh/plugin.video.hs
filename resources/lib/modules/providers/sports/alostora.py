# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from resources.lib.modules.globals import g
from resources.lib.modules.providers.handlers.Alba_player import AlbaPlayer

from resources.lib.modules.providers.sports.sports_provider import SportsProvider


class Alostora(SportsProvider):
    def __init__(self):
        super().__init__(
            'الاسطورة',
            "alostora",
            ["https://livehd7.live/"],
        )

    def get_games_list(self) -> list:
        def construct_title(game_div):
            return self._generate_title(
                game_div.find('div', class_='team-first').find('div', {'class': re.compile(".*team_title")}).get_text(),
                game_div.find('div', class_='team-second').find('div', {'class': re.compile(".*team_title")}).get_text(),
                game_div.find('div', {'class': 'matchTime'}).get_text()
            )

        def construct_poster(game_div):
            return self._generate_game_art(
                game_div.find('div', class_='team-first').find('img').get('src'),
                game_div.find('div', class_='team-first').find('div', {'class': re.compile(".*team_title")}).get_text(),
                game_div.find('div', class_='team-second').find('img').get('src'),
                game_div.find('div', class_='team-second').find('div', {'class': re.compile(".*team_title")}).get_text(),
                banner=True
            )

        def construct_overview(game_div):
            info = game_div.find(class_='events-info')
            return self._generate_overview(
                info.select_one('span.mic').get_text(),
                info.select_one('span.tv').get_text(),
                info.select_one('span.cup').get_text(),
                '-'.join(map(lambda r: r.get_text(), game_div.find(class_='matchResult').find_all(class_='result')))
            )

        page = self.requests.get().text
        games = self._extract_posts_meta(
            page, g.MEDIA_MOVIE,
            lambda soup: soup.find('div', id="today").div,
            title=construct_title,
            poster=construct_poster,
            url=lambda post_tag: post_tag.a.get('href'),
            overview=construct_overview,
            last_watched_at= lambda post_tag: 'finshed' if 'finshed' in post_tag['class'] else None,
            edit_meta=self._improve_game_meta
        )

        # TODO: find a better way
        sorted_games = []
        finished_games = []
        for game in games:
            if game['info'].get('last_watched_at'):
                finished_games.append(game)
            else:
                sorted_games.append(game)
        sorted_games.extend(finished_games)

        return sorted_games

    def get_sources(self, url: str):
        page = self.requests.get(url).text
        return self._extract_sources_meta(
            page,
            lambda soup: AlbaPlayer.get_sources(soup, url),
            provider=lambda source_div: source_div.get_text(),
            quality=lambda source_div: 'livestream',
            url=lambda source_div: AlbaPlayer.get_url(source_div, url),
            type=lambda source_div: 'livestream'
        )