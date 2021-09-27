# -*- coding: utf-8 -*-

from resources.lib.debrid.real_debrid import RealDebrid


class RealDebridResolver:
    """
    Resolver for Real Debrid
    """
    def __init__(self):
        self.debrid_module = RealDebrid()
        self._source_normalization = (
            ("path", "path", None),
            ("bytes", "size", lambda k: (k / 1024) / 1024),
            ("size", "size", None),
            ("filename", "release_title", None),
            ("id", "id", None),
            ("link", "link", None),
            ("selected", "selected", None),
        )
        self.torrent_id = None

    def resolve_stream_url(self, file_info):
        """
        Convert provided source file into a link playable through debrid service
        :param file_info: Normalised information on source file
        :return: streamable link
        """
        return self.debrid_module.resolve_hoster(file_info["link"])

    # def resolve_stream_url(self, source):
    #     stream_link = None
    #     try:
    #         stream_link = self.debrid_module.resolve_hoster(source)
    #     except:
    #         pass
    #     return stream_link
