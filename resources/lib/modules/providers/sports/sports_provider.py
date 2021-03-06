# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import datetime

from resources.lib.common.tools import get_current_datetime_for_time
from resources.lib.modules.globals import g
from resources.lib.modules.providers.provider import Provider


class SportsProvider(Provider):
    def __init__(self, display_name: str, name: str, urls: list):
        super().__init__(display_name, name, urls)

    def get_games_list(self) -> list:
        return []

    def get_sources(self, url: str) -> list:
        return []

    def _generate_title(self, first_team_name, second_team_name, playing_time):
        return '{} ضد {} الساعة {}'.format(
            first_team_name,
            second_team_name,
            playing_time
        )

    def _generate_overview(self, commentator, channel, league, results=None):
        return '''
        النتيجة: {}
        المعلق: {}
        القناة: {}
        الدوري: {}
        '''.format(results or '-', commentator, channel, league)

    def _improve_game_meta(self, game):
        playing_time = game['info']['title'].split('الساعة')[1]
        try:
            game['info']['aired'] = get_current_datetime_for_time(playing_time, g.DATE_TIME_FORMAT)
        except Exception:
            pass
        if game['info'].get('last_watched_at'):
            game['info']['last_watched_at'] = game['info']['aired'] or datetime.datetime.today().strftime(g.DATE_TIME_FORMAT)
        game['info']['duration'] = 6300
        game['info']['genre'] = ['sports']