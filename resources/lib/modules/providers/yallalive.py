# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from resources.lib.common.exceptions import try_and_log
from resources.lib.modules.globals import g

from bs4 import BeautifulSoup
from resources.lib.modules.providers.provider import Provider


class Yallalive(Provider):
    def __init__(self):
        super().__init__(
            'يلا لايف',
            "yallalive",
            ["https://yallalive.io/"],
        )

    @try_and_log()
    def get_games_list(self) -> list:
        games = []
        response = self.requests.get()
        soup = BeautifulSoup(response.text, 'html.parser')

        from collections import defaultdict
        for gameDiv in soup.find('div', id="today").div:
            game = defaultdict(dict)

            first_team = gameDiv.find('div', class_='team-first')
            second_team = gameDiv.find('div', class_='team-second')

            game['info']['title'] = '{} ضد {} الساعة {}'.format(
                first_team.find('div', {'class': re.compile(".*team_title")}).get_text(),
                second_team.find('div', {'class': re.compile(".*team_title")}).get_text(),
                gameDiv.find('div', {'class': 'matchTime'}).get_text(),
            )

            game['art']['poster'] = self._generate_game_poster(
                first_team.find('div', {'class': re.compile(".*logo")}).img['src'],
                second_team.find('div', {'class': re.compile(".*logo")}).img['src']
            )
            game['info']['mediatype'] = g.MEDIA_MOVIE

            game['url'] = gameDiv.a.get('href')
            game['provider'] = self.name

            game['args'] = g.create_args(game)
            games.append(game)

        return games

    @try_and_log()
    def get_sources(self, url: str):
        sources = []
        # TODO:
        return sources