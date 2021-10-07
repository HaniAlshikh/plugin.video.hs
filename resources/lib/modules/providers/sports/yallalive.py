# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from resources.lib.modules.globals import g

from resources.lib.modules.providers.sports.sports_provider import SportsProvider


class Yallalive(SportsProvider):
    def __init__(self):
        super().__init__(
            'يلا لايف',
            "yallalive",
            ["https://yallalive.io/"],
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
                    game_div.find('div', class_='team-first').find('div', {'class': re.compile(".*logo")}).img['src'],
                    game_div.find('div', class_='team-first').find('div', {'class': re.compile(".*team_title")}).get_text(),
                    game_div.find('div', class_='team-second').find('div', {'class': re.compile(".*logo")}).img['src'],
                    game_div.find('div', class_='team-second').find('div', {'class': re.compile(".*team_title")}).get_text(),
                    banner=True
                )
            except Exception:
                return ''

        return self._extract_posts_meta(
            page, g.MEDIA_MOVIE,
            lambda soup: soup.find('div', id="yestrday").div,
            title=get_title,
            poster=get_poster,
            # url=lambda post_tag: post_tag.a.get('href'), TODO
            edit_meta=self._improve_game_meta,
        )

    def get_sources(self, url: str):
        sources = []
        # TODO:
        return sources