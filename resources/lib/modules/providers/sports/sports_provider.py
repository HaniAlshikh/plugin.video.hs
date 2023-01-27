# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g
from resources.lib.modules.providers.provider import Provider


class SportsProvider(Provider):
    def __init__(self, display_name: str, name: str, urls: list):
        super().__init__(display_name, name, urls)

    def get_games_list(self) -> list:
        return []

    def get_sources(self, url: str) -> list:
        return []

    def _get_channel_sources(self, channel: str):
        from resources.lib.modules.providers.media.MagicHD import MagicHD
        provider = MagicHD()  # TODO: abstract
        channels = []
        while len(channels) == 0:
            g.log("trying to find channel sources for {}".format(channel))
            channels = provider.search(channel, g.MEDIA_CHANNEL)
            channel = channel.rsplit(' ', 1)[0] # remove last word for more general search
        from resources.lib.modules.metadata_handler import MetadataHandler
        return [self._get_source_meta(
            display_name=MetadataHandler.get_media(ch, 'display_name'),
            url=MetadataHandler.get_media(ch, 'url'),
            release_title=MetadataHandler.get_media(ch, 'title'),
            quality="livestream",
            type="hoster",
            provider=provider.name,
            channel=MetadataHandler.get_media(ch, 'title'),
        ) for ch in channels]