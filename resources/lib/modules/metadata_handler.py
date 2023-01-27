# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from datetime import datetime

from resources.lib.common.tools import clean_up_string, parse_datetime
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
        if params.get('first_team'): media['info']['first_team'] = params.get('first_team')
        if params.get('second_team'): media['info']['second_team'] = params.get('second_team')
        if params.get('aired'): media['info']['aired'] = params.get('aired')
        if params.get('channel'): media['info']['channel'] = params.get('channel')
        if params.get('result'): media['info']['result'] = params.get('result')
        if params.get('commentator'): media['info']['commentator'] = params.get('commentator')
        if params.get('league'): media['info']['league'] = params.get('league')

        if params.get('poster'): media['art']['poster'] = params.get('poster')

        if params.get('url'): media['url'] = params.get('url')
        if params.get('provider'): media['provider'] = params.get('provider')

        media['args'] = g.create_args(media)
        return media

    @staticmethod
    def get_media(media, id):
        if id == 'info': return media.get('info')
        if id == 'title': return media.get('info', {}).get('title')
        if id == 'overview': return media.get('info', {}).get('overview')
        if id == 'last_watched_at': return media.get('info', {}).get('last_watched_at')
        if id == 'mediatype': return media.get('info', {}).get('mediatype')
        if id == 'category': return media.get('info', {}).get('category')
        if id == 'tvshowtitle': return media.get('info', {}).get('tvshowtitle')
        if id == 'season': return media.get('info', {}).get('season')
        if id == 'episode': return media.get('info', {}).get('episode')
        if id == 'first_team': return media.get('info', {}).get('first_team')
        if id == 'second_team': return media.get('info', {}).get('second_team')
        if id == 'aired': return media.get('info', {}).get('aired')
        if id == 'channel': return media.get('info', {}).get('channel')
        if id == 'result': return media.get('info', {}).get('result')
        if id == 'commentator': return media.get('info', {}).get('commentator')
        if id == 'league': return media.get('info', {}).get('league')

        if id == 'art': return media.get('art')
        if id == 'poster': return media.get('art', {}).get('poster')

        if id == 'url': return media.get('url')
        if id == 'provider': return media.get('provider')

        if id == 'args': return media.get('args')

        return None

    @staticmethod
    def source(**params):
        source = {}

        if params.get('display_name'): source['display_name'] = params.pop('display_name')
        if params.get('release_title'): source['release_title'] = params.pop('release_title')
        if params.get('url'): source['url'] = params.pop('url')
        if params.get('quality'): source['quality'] = params.pop('quality')
        if params.get('type'): source['type'] = params.pop('type')
        if params.get('provider'): source['provider'] = params.pop('provider')
        if params.get('origin'): source['origin'] = params.pop('origin')
        if params.get('channel'): source['channel'] = params.pop('channel')

        return source

    @staticmethod
    def improve_media(item):
        if item.get('info'):
            if item['info'].get("mediatype", "") == g.MEDIA_SPORT:
                item['info']['title'] = '{} ضد {} الساعة {} القناة {}'.format(
                    item['info'].get('first_team', 'غير معروف'),
                    item['info'].get('second_team', 'غير معروف'),
                    str((parse_datetime(item['info'].get('aired'), g.DATE_TIME_FORMAT, time_only=True) or ''))[0:5],
                    item['info'].get('channel', 'غير معروف'),
                )

                item['info']['overview'] = '''
                النتيجة: {}
                المعلق: {}
                القناة: {}
                الدوري: {}
                '''.format(
                    item['info'].get('result', '-'),
                    item['info'].get('commentator', 'غير معروف'),
                    item['info'].get('channel', 'غير معروف'),
                    item['info'].get('league', 'غير معروف'),
                )

                if item['info'].get('last_watched_at'):
                    item['info']['last_watched_at'] = item['info'].get('aired') or datetime.today().strftime(g.DATE_TIME_FORMAT)
                if not item['info'].get('duration'):
                    item['info']['duration'] = 6300
                if not item['info'].get('genre'):
                    item['info']['genre'] = ['sports']

                item['info']['mediatype'] = g.MEDIA_MOVIE  # TODO: otherwise no red title for finished games

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

        item['args'] = g.create_args(item)

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
