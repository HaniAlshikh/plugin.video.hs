# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.common.tools import clean_up_string
from resources.lib.modules.globals import g
from resources.lib.modules.providers.provider_utils import get_info, get_quality


class MetadataHandler:

    @staticmethod
    def media(**params):
        from collections import defaultdict
        media = defaultdict(dict)

        if params.get('title'): media['info']['title'] = params.get('title')
        if params.get('overview'): media['info']['overview'] = params.get('overview')
        if params.get('last_watched_at'): media['info']['last_watched_at'] = params.get('last_watched_at')
        if params.get('mediatype'): media['info']['mediatype'] = params.get('mediatype')
        if params.get('category'): media['info']['category'] = params.get('category')
        if params.get('tvshowtitle'): media['info']['tvshowtitle'] = params.get('tvshowtitle')
        if params.get('season'): media['info']['season'] = params.get('season')
        if params.get('episode'): media['info']['episode'] = params.get('episode')

        if params.get('poster'): media['art']['poster'] = params.get('poster')

        if params.get('url'): media['url'] = params.get('url')
        if params.get('provider'): media['provider'] = params.get('provider')

        media['args'] = g.create_args(media)
        return media

    @staticmethod
    def get_media(media, id):
        if id == 'info': return media['info']
        if id == 'title': return media['info']['title']
        if id == 'overview': return media['info']['overview']
        if id == 'last_watched_at': return media['info']['last_watched_at']
        if id == 'mediatype': return media['info']['mediatype']
        if id == 'category': return media['info']['category']
        if id == 'tvshowtitle': return media['info']['tvshowtitle']
        if id == 'season': return media['info']['season']
        if id == 'episode': return media['info']['episode']

        if id == 'art': return media['art']
        if id == 'poster': return media['art']['poster']

        if id == 'url': return media['url']
        if id == 'provider': return media['provider']

        if id == 'args': return media['args']

        return None

    @staticmethod
    def source(**params):
        source = {}

        source['display_name'] = params.get('display_name')
        source['release_title'] = params.get('release_title')
        source['url'] = params.get('url')
        source['quality'] = params.get('quality')
        source['type'] = params.get('type')
        source['provider'] = params.get('provider')
        source['origin'] = params.get('origin')

        return source

    @staticmethod
    def improve_media(item):
        if item.get('info'):
            if item['info'].get('title'):
                item['info']['title'] = clean_up_string(item['info']['title'])
                try:
                    num = int(item['info']['title'])
                    if item['info'].get("mediatype", "") == g.MEDIA_SEASON:
                        item['info']['title'] = "{} {}".format('موسم', num)
                    else:
                        item['info']['title'] = "{} {}".format('حلقة', num)
                except:
                    pass

            if item['info'].get('overview') and not item['info'].get('plot'):
                item['info']['plot'] = item['info']['overview']

            if item['info'].get('plot') and not item['info'].get('plotoutline'):
                item['info']['plotoutline'] = item['info']['plot']

            if item['info'].get('plot') and not item['info'].get('overview'):
                item['info']['overview'] = item['info']['plot']

        if item.get('url'):
            item['url'] = str(item['url']).strip()

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
        item['quality'] = get_quality(item.get('quality'))

        if not item.get('provider'):
            from urllib.parse import urlparse
            item['provider'] = urlparse(item['url']).netloc
        if 'خاص' in item['provider']:
            item['display_name'] = item['provider'] + ' ' + item['quality']

        if not item.get('display_name'):
            item['display_name'] = item['provider'] + ' ' + item['quality']

        if item.get('display_name'):
            item['display_name'] = clean_up_string(item['display_name'])

        if item.get('release_title'):
            item['release_title'] = clean_up_string(item['release_title'])
            item['info'] = get_info(item['release_title'])

        if item.get('url'):
            item['url'] = str(item['url']).strip()
