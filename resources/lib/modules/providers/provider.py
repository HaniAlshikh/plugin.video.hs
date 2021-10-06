# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os

import bs4
from bs4 import BeautifulSoup

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

    def _get_current_page_number(self, soup: bs4.BeautifulSoup) -> int:
        pass


    def _extract_categories_meta(self, html, categories_div,  cat_title, cat_url):
        categories = []
        soup = BeautifulSoup(html, 'html.parser')
        cat = {}
        for cat_tag in categories_div(soup):
            cat['title'] = cat_title(cat_tag)
            cat['url'] = cat_url(cat_tag)
        return categories

    def _extract_post_meta(self, html: str, mediatype, posts_tag: callable, **params) -> list:
        posts = []
        soup = BeautifulSoup(html, 'html.parser')

        from collections import defaultdict
        duplicates = {}  # used mostly to filter episodes
        for post_tag in posts_tag(soup):
            poster = params.get('poster')(post_tag) if params.get('poster') else ''
            if mediatype == g.MEDIA_SHOW and poster and duplicates.get(poster):
                continue

            post = defaultdict(dict)
            post['info']['title'] = params.get('title')(post_tag)
            post['info']['mediatype'] = mediatype

            post['art']['poster'] = poster

            post['url'] = params.get('url')(post_tag)
            post['provider'] = params.get('provider')
            post['args'] = g.create_args(post)

            posts.append(post)
            duplicates[poster] = post

        if params.get('include_page'):
            page = self._get_current_page_number(soup)
            if page:
                posts.append(page + 1)

        return posts

    @staticmethod
    def _generate_game_art(
            first_img: str, first_img_title: str, second_img: str, second_img_title: str, banner=False
    ) -> str:
        first_img_title = '_'.join(first_img_title.split())
        second_img_title = '_'.join(second_img_title.split())

        extension = '_banner.png' if banner else '.png'
        poster_path = os.path.join(g.TMP_PATH, first_img_title+'vs'+second_img_title+extension)
        poster_path_reversed = os.path.join(g.TMP_PATH, second_img_title+'vs'+first_img_title+extension)
        if not os.path.exists(poster_path):
            if os.path.exists(poster_path_reversed):
                return poster_path_reversed
            from resources.lib.common.image_generator import combine_vs
            poster = combine_vs(first_img, second_img, banner)
            poster.save(poster_path, format='png')

        return poster_path