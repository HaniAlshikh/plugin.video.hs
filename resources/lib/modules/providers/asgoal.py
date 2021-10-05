# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from resources.lib.common.exceptions import try_and_log
from resources.lib.common.tools import clean_up_string, get_current_datetime_for_time
from resources.lib.modules.globals import g

from bs4 import BeautifulSoup
from resources.lib.modules.providers.provider import Provider


class Asgoal(Provider):
    def __init__(self):
        super().__init__(
            'اس جول',
            "asgoal",
            ["https://www.as-goal.com/"],
        )

    def get_games_list(self) -> list:
        games = []
        response = self.requests.get('m/')
        soup = BeautifulSoup(response.text, 'html.parser')

        from collections import defaultdict
        for gameDiv in soup.find('div', id="today").select('a.AlbaSposrTable'):
            game = defaultdict(dict)

            first_team = gameDiv.find('div', class_='AlbaTableFteam')
            second_team = gameDiv.find('div', class_='AlbaTableSteam')
            first_team_name = clean_up_string(first_team.get_text())
            second_team_name = clean_up_string(second_team.get_text())
            playing_time = clean_up_string(gameDiv.find(
                'div', class_='AlbaTableMtime').find('div', {'class': re.compile('.*time.*')}).get_text())

            game['info']['title'] = '{} ضد {} الساعة {}'.format(
                first_team_name,
                second_team_name,
                playing_time
            )
            game['info']['premiered'] = get_current_datetime_for_time(playing_time, g.DATE_TIME_FORMAT)
            game['info']['duration'] = 6300
            game['info']['genre'] = ['sports']
            game['info']['mediatype'] = g.MEDIA_MOVIE

            try:
                game['art']['poster'] = self._generate_game_art(
                    first_team.img['src'],
                    first_team_name,
                    second_team.img['src'],
                    second_team_name,
                    banner=True
                )
            except Exception:
                pass

            # game['url'] = gameDiv.a.get('href') # TODO:
            game['provider'] = self.name
            game['args'] = g.create_args(game)

            games.append(game)

        return games

    @try_and_log()
    def get_sources(self, url: str):
        sources = []
        # TODO:
        return sources