# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.common.tools import clean_up_string
from resources.lib.modules.globals import g
from resources.lib.modules.providers.provider_utils import get_info


class MetadataHandler:

    @staticmethod
    def media(**params):
        from collections import defaultdict
        media = defaultdict(dict)

        media['info']['title'] = params.get('title')
        media['info']['mediatype'] = params.get('mediatype')

        media['art']['poster'] = params.get('poster')

        media['url'] = params.get('url')
        media['provider'] = params.get('provider')
        media['args'] = g.create_args(media)

        return media

    @staticmethod
    def improve_media(item):
        item['info']['title'] = clean_up_string(item['info']['title'])

        if item.get('url'):
            item['url'] = item['url'].strip()

        if item.get('art'):
            if item['art'].get('poster'):
                if not item['art'].get('fanart'): item['art']['fanart'] = item['art']['poster']

                landscape = item['art']['landscape'] if item['art'].get('landscape') else item['art']['poster']
                if not item['art'].get('banner'): item['art']['banner'] = landscape
                if not item['art'].get('landscape'): item['art']['landscape'] = landscape
                if not item['art'].get('thumb'): item['art']['thumb'] = landscape

            clearlogo = item['art'].get('clearlogo')
            clearart = item['art'].get('clearart')
            if not clearlogo: clearlogo = clearart
            if not clearart: clearart = clearlogo
            item['art']['clearlogo'] = clearlogo
            item['art']['clearart'] = clearart

    @staticmethod
    def improve_source(item):
        if item.get('display_name'):
            item['display_name'] = clean_up_string(item['display_name'])

        if item.get('release_title'):
            item['release_title'] = clean_up_string(item['release_title'])
            item['info'] = get_info(item['release_title'])

        if not item.get('provider'):
            item['provider'] = item['origin']
        if 'خاص' in item['provider']:
            item['display_name'] = item['provider'] + ' ' + item['quality']

        if item.get('url'):
            item['url'] = item['url'].strip()