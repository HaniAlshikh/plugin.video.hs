# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from urllib.parse import urlparse

import requests

from resources.lib.modules.globals import g
from resources.lib.modules.scrapers.request import Request as R


class Request:
    def __init__(self, base: str):
        self.base = base
        self.request = R()

    def get(self, url: str = '', headers: dict = None):
        url = self.prep_url(url)
        g.log('GET: Requesting: ' + url)
        r = self.request.get(url, headers=headers)
        r.encoding = 'utf-8'
        return r

    def post(self, url, data, headers: dict = None):
        url = self.prep_url(url)
        g.log('POST: Requesting: ' + url)
        r = self.request.post(url, data, headers)
        r.encoding = 'utf-8'
        return r

    def prep_url(self, url):
        url = self.base + url if not url.startswith('http') else url
        url = url.strip()
        url = url.replace(' ', '+') if any(s in url for s in ['?s', 'search']) else url.replace(' ', '-')
        return url
