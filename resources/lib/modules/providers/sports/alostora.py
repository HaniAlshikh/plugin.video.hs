# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

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
        def construct_poster(game_div):
            return self._generate_game_art(
                game_div.find('div', class_='AF_FTeam').find('img').get('src'),
                game_div.find('div', class_='AF_FTeam').find('div', class_='AF_TeamName').get_text(),
                game_div.find('div', class_='AF_STeam').find('img').get('src'),
                game_div.find('div', class_='AF_STeam').find('div', class_='AF_TeamName').get_text(),
                banner=True
            )

        def construct_air_datetime(game_div):
            time = game_div.find('div', class_='AF_EvTime').get_text()
            try:
                from resources.lib.common.tools import get_current_datetime_for_time
                return get_current_datetime_for_time(time, g.DATE_TIME_FORMAT)
            except Exception:
                return time

        page = self.requests.get().text
        return self._extract_posts_meta(
            page, g.MEDIA_SPORT,
            lambda soup: soup.find('div', id="yestrday").div,
            first_team=lambda game_div: game_div.find('div', class_='AF_FTeam').find('div', class_='AF_TeamName').get_text(),
            second_team=lambda game_div: game_div.find('div', class_='AF_STeam').find('div', class_='AF_TeamName').get_text(),
            aired=construct_air_datetime,
            channel=lambda game_div: game_div.find(class_='AF_EvInfo').select_one('span.tv').get_text(),
            result=lambda game_div: '-'.join(map(lambda r: r.get_text(), game_div.find(class_='AF_EventResult').find_all(class_='result'))),
            commentator=lambda game_div: game_div.find(class_='AF_EvInfo').select_one('span.mic').get_text(),
            league=lambda game_div: game_div.find(class_='AF_EvInfo').select_one('span.cup').get_text(),
            poster=construct_poster,
            url=lambda game_div: game_div.a.get('href') + "&channel=" + game_div.find(class_='AF_EvInfo').select_one('span.tv').get_text(),
            last_watched_at= lambda game_div: 'finshed' if 'finshed' in game_div['class'] else None,
        )

    def get_sources(self, url: str):
        url, ch = url.split("&channel=")  # TODO: abstract me
        results = self._get_channel_sources(ch)
        page = self.requests.get(url).text
        results.extend(self._extract_sources_meta(
            page,
            lambda soup: AlbaPlayer.get_sources(soup, url),
            provider=lambda source_div: source_div.get_text(),
            quality=lambda source_div: 'livestream',
            url=lambda source_div: AlbaPlayer.get_url(source_div, url),
            type=lambda source_div: 'livestream'
        ))
        return results
