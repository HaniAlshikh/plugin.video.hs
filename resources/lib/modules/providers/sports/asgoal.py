# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.providers.handlers.Alba_player import AlbaPlayer

from resources.lib.modules.providers.sports.sports_provider import SportsProvider


class Asgoal(SportsProvider):
    def __init__(self):
        super().__init__(
            'اس جول',
            "asgoal",
            ["https://www.as-goal.com/"],
        )

    def get_games_list(self) -> list:
        def construct_title(game_div):
            return self._generate_title(
                game_div.find('div', class_='AlbaTableFteam').get_text(),
                game_div.find('div', class_='AlbaTableSteam').get_text(),
                game_div.find('div', class_='AlbaTableMtime').div.get_text()
            )

        def construct_poster(game_div):
            return self._generate_game_art(
                game_div.find('div', class_='AlbaTableFteam').img['src'],
                game_div.find('div', class_='AlbaTableFteam').get_text(),
                game_div.find('div', class_='AlbaTableSteam').img['src'],
                game_div.find('div', class_='AlbaTableSteam').get_text(),
                banner=True
            )

        def construct_overview(game_div):
            info = game_div.find(class_='AlbaTableMinfo')
            return self._generate_overview(
                ' '.join(info.find(class_='fa-microphone').parent.stripped_strings),
                ' '.join(info.find(class_='fa-tv-retro').parent.stripped_strings),
                ' '.join(info.find(class_='fa-trophy').parent.stripped_strings),
                ' '.join(game_div.find(class_='matchResult').stripped_strings) if game_div.find(class_='matchResult')
                else ''
            )

        page = self.requests.get('m/').text
        return self._extract_posts_meta(
            page, g.MEDIA_MOVIE,
            lambda soup: soup.find('div', id="Today").select('a.AlbaSposrTable'),
            title=construct_title,
            poster=construct_poster,
            url=lambda post_tag: post_tag.get('href'),
            overview=construct_overview,
            last_watched_at= lambda post_tag: 'finshed' if 'finshed' in post_tag['class'] else None,
            edit_meta=self._improve_game_meta
        )

    def get_sources(self, url: str):
        page = self.requests.get(url).text
        return self._extract_sources_meta(
            page,
            # lambda soup: soup.find(class_="servers-name").find_all("button"), TODO
            lambda soup: AlbaPlayer.get_sources(soup, url),
            provider=lambda source_div: source_div.get_text(),
            quality=lambda source_div: 'livestream',
            url=lambda source_div: AlbaPlayer.get_url(source_div, url),
            type=lambda source_div: 'livestream'
        )