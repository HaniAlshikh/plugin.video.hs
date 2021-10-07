# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from urllib.parse import urlparse

import requests

from resources.lib.modules.globals import g


class Request:
    def __init__(self, base: str):
        self.base = base

    def get(self, url: str = ''):
        url = self.prep_url(url)
        g.log('GET: Requesting: ' + url)
        r = requests.get(url)
        r.encoding = 'utf-8'
        return r

    def post(self, url: str = '', data: dict = {}):
        url = self.prep_url(url)
        g.log('POST: Requesting: ' + url)
        r = requests.post(url, data)
        r.encoding = 'utf-8'
        return r

    def prep_url(self, url):
        url = self.base + url if urlparse(self.base).netloc not in url else url
        url = url.strip()
        url = url.replace(' ', '+') if any(s in url for s in ['?s', 'search']) else url.replace(' ', '-')
        return url
