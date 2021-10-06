# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from urllib.parse import urlparse

import requests

from resources.lib.modules.globals import g


class Request:
    def __init__(self, base: str):
        self.base = base

    def get(self, page: str = ''):
        page = self.base + page if urlparse(self.base).netloc not in page else page
        page = page.replace(' ', '+') if any(s in page for s in ['?s', 'search']) else page.replace(' ', '-')
        g.log('GET: Requesting: ' + page)
        r = requests.get(page)
        r.encoding = 'utf-8'
        return r

    def post(self, page: str = '', data: dict = {}):
        page = self.prep_url(page)
        g.log('POST: Requesting: ' + page)
        r = requests.post(page, data)
        r.encoding = 'utf-8'
        return r

    def prep_url(self, page):
        page = self.base + page if urlparse(self.base).netloc not in page else page
        page = page.replace(' ', '+') if any(s in page for s in ['?s', 'search']) else page.replace(' ', '-')
        return page
