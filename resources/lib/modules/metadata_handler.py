# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.providers.provider_utils import get_info
from urllib.parse import urlparse
from resources.lib.debrid.real_debrid import RealDebrid

class MetadataHandler:

    @staticmethod
    def improve_media(item):
        if item.get('art'):
            if item['art'].get('poster'):
                if not item['art'].get('fanart'): item['art']['fanart'] = item['art']['poster']
                if not item['art'].get('banner'): item['art']['banner'] = item['art']['poster']
                if not item['art'].get('landscape'): item['art']['landscape'] = item['art']['poster']
                if not item['art'].get('thumb'): item['art']['thumb'] = item['art']['poster']

    @staticmethod
    def improve_source(item):
        item['info'] = get_info(item['release_title'])

        if 'خاص' in item['provider']:
            item['provider'] = item['origin']
            item['display_name'] = item['provider'] + ' ' + item['quality']