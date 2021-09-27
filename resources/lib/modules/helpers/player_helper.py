# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g


class PlayerHelper:
    def __init__(self, media_info):
        self.source = media_info['sources'].pop()
        self.media_info = media_info

    @staticmethod
    def ensure_all_sources_were_tried(media_info: dict) -> None:
        if not media_info.get('sources'):
            g.log('missing sources for: {}'.format(p.media_info['info']['title']), 'error')
            return

        p = PlayerHelper(media_info)
        stream_link = p._resolve([p.source])
        if stream_link:
            player = p._play_link(stream_link)
            while not g.is_window_visible('fullscreenvideo'):
                g.log('waiting for Player to process: ' + stream_link)
                if g.is_window_visible('okdialog'):
                    g.log('faild to play: ' + stream_link)
                    break
                g.sleep(500)

            if player.isPlaying():
                g.log('found working source: ' + p.source['display_name'])
                return

        if media_info['sources']:
            g.play_media('getSources', action_args=g.create_args(p.media_info))
        else:
            g.ok_dialog('تعذر العثور على روابط للتشغيل')

    def _play_link(self, link: str):
        g.log('Playing: ' + link)
        from resources.lib.modules import player
        hs_player = player.HSPlayer()
        hs_player.play_source(
            link, self.media_info, resume_time=0
        )
        return hs_player

    def _resolve(self, sources: list) -> str:
        from resources.lib.modules.helpers.resolver_helper import ResolverHelper
        stream_link = ResolverHelper().resolve_silent_or_visible(self.media_info)
        return stream_link

