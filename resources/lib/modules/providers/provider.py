# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os

from bs4 import BeautifulSoup

from resources.lib.database import Database
from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.providers.provider_utils import get_quality
from resources.lib.modules.request import Request


class Provider:
    def __init__(self, display_name: str, name: str, urls: list):
        self.display_name = display_name
        self.name = name
        self.urls = urls
        self.requests = Request(self.urls[0])

        self.support_channels = False

        self.notification_header = g.ADDON_NAME + ": " + self.display_name
        self.progress_dialog = g.progress_notification(self.notification_header, "", silent=True)

    def _extract_categories_meta(self, page, categories_div, cat_title, cat_url):
        categories = []
        soup = BeautifulSoup(page, 'html.parser')
        for cat_tag in categories_div(soup):
            categories.append({
                'title': cat_title(cat_tag),
                'url': cat_url(cat_tag)
            })
        return categories

    def _extract_posts_meta(self, page: str, mediatype, posts_tag: callable, **params) -> list:
        posts = []
        soup = BeautifulSoup(page, 'html.parser')

        duplicates = {}  # used mostly to filter episodes
        for post_tag in posts_tag(soup):
            poster = (params.get('poster') or self._none)(post_tag)
            if mediatype == g.MEDIA_SHOW and poster and duplicates.get(poster):
                continue

            post = MetadataHandler.media(
                title=(params.get('title') or self._none)(post_tag),
                mediatype=mediatype,
                poster=poster,
                url=(params.get('url') or self._none)(post_tag),
                provider=self.name,
                overview=(params.get('overview') or self._none)(post_tag),
                last_watched_at=(params.get('last_watched_at') or self._none)(post_tag)
            )

            if params.get('edit_meta'):
                params['edit_meta'](post)

            posts.append(post)
            duplicates[poster] = post

        # TODO: make it smarter
        g.PAGE = self._extract_current_page_number(soup) if params.get('include_page') else -1

        return posts

    def _extract_current_page_number(self, soup, **params):
        pages_tag = params.get('pages_tag')
        pages_tag = pages_tag(soup) if pages_tag else soup.find('ul', class_='page-numbers')
        if not pages_tag:
            return -1

        page_num = pages_tag.select_one('li.active > a')
        if page_num:
            return int(page_num.get_text())

        page_num = pages_tag.select_one('span.current')
        if page_num:
            return int(page_num.get_text())

        if params.get('selectors'):
            for selector in params.get('selectors'):
                page_num = selector(pages_tag)
                if page_num:
                    g.log('Current Page: ' + page_num.get_text())
                    return int(page_num.get_text())
        return -1

    def _extract_sources_meta(self, page: str, sources_tag: callable, **params) -> list:
        sources = []

        soup = BeautifulSoup(page, 'html.parser')
        for source_tag in sources_tag(soup):
            source = MetadataHandler.source(
                display_name=(params.get('display_name') or self._none)(source_tag),
                release_title=(params.get('release_title') or self._none)(source_tag),
                url=(params.get('url') or self._none)(source_tag),
                quality=(params.get('quality') or self._none)(source_tag),
                type=(params.get('type') or self._none)(source_tag),
                provider=(params.get('provider') or self._none)(source_tag),
                origin=self.name,
            )
            sources.append(source)

        return sources

    def _extract_m3u_meta(self, media: dict, mediatype: str, **params) -> dict:
        return MetadataHandler.media(
            title=params.get('title') or media['name'],
            mediatype=mediatype,
            poster=params.get('poster') or media['logo'],
            url=params.get('url') or media['url'],
            provider=self.name,
            overview=params.get('overview'),
            category=params.get('category'),
            tvshowtitle=params.get('tvshowtitle'),
            episode=params.get('episode'),
            season=params.get('season'),
        )

    def _get_source_meta(self, **params) -> list:
        return MetadataHandler.source(
            display_name=params.get('display_name'),
            release_title=params.get('release_title'),
            url=params.get('url'),
            quality=params.get('quality'),
            type=params.get('type'),
            provider=params.get('provider'),
            origin=self.name,
        )

    def _extract_m3u(self):
        g.log("Downloading...")
        self.progress_dialog.update(10, self.notification_header, "جاري تحميل ملف الروابط")
        from resources.lib.third_part.m3u_parser import M3uParser
        parser = M3uParser()
        parser.parse_m3u(self.urls[0], check_live=False, enforce_schema=True)
        return parser

    @staticmethod
    def _generate_game_art(
            first_img: str, first_img_title: str, second_img: str, second_img_title: str, banner=False
    ) -> str:
        g.log('Generating art for: {} vs {}'.format(first_img_title, second_img_title))
        try:
            first_img_title = '_'.join(first_img_title.split())
            second_img_title = '_'.join(second_img_title.split())

            extension = '_banner.png' if banner else '.png'
            poster_path = os.path.join(g.TMP_PATH, first_img_title + 'vs' + second_img_title + extension)
            poster_path_reversed = os.path.join(g.TMP_PATH, second_img_title + 'vs' + first_img_title + extension)
            if not os.path.exists(poster_path):
                if os.path.exists(poster_path_reversed):
                    return poster_path_reversed
                from resources.lib.common.image_generator import combine_vs
                poster = combine_vs(first_img, second_img, banner)
                poster.save(poster_path, format='png')

            return poster_path
        except Exception as e:
            g.log(str(e), 'error')

    @staticmethod
    def _none(*args):
        return None
