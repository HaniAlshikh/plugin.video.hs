# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import requests

from resources.lib.modules.globals import g


class Request:
    def __init__(self, base: str):
        self.base = base

    def get(self, page: str = ''):
        page = self.base + page if self.base not in page else page
        page = page.replace(' ', '+') if '?s' or 'search' in page else page.replace(' ', '-')
        g.log('GET: Requesting: ' + page)
        r = requests.get(page)
        r.encoding = 'utf-8'
        return r
