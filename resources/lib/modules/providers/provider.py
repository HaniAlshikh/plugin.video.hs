# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os

from resources.lib.modules.globals import g
from resources.lib.modules.request import Request


class Provider:
    def __init__(self, display_name: str, name: str, urls: list):
        self.display_name = display_name
        self.name = name
        self.urls = urls
        self.requests = Request(self.urls[0])

    def movies(self, category: str = None):
        pass

    def tv_shows(self, category: str = None):
        pass

    def resolve(self, url):
        return url

    def search(self, query, mediatype: str):
        return []

    @staticmethod
    def _generate_game_poster(first_img: str, second_img: str) -> str:
        first_img_title = first_img.split('/')[-1].split('.')[0]
        second_img_title = second_img.split('/')[-1].split('.')[0]

        poster_path = g.TMP_PATH + '/' + first_img_title + '-' + second_img_title + '.png'
        poster_path_reversed = g.TMP_PATH + '/' + second_img_title + '-' + first_img_title + '.png'
        if not os.path.exists(poster_path):
            if os.path.exists(poster_path_reversed):
                return poster_path_reversed
            from resources.lib.common.image_generator import combine_vs
            poster = combine_vs(first_img, second_img)
            poster.save(poster_path)

        return poster_path