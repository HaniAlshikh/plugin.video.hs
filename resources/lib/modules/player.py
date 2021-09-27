# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import copy

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.common import tools
from resources.lib.modules.globals import g


class HSPlayer(xbmc.Player):
    """
    Class to handle playback methods and accept callbacks from Kodi player
    """

    def __init__(self):
        super(HSPlayer, self).__init__()

        self.item_information = None
        self.mediatype = None
        self.playing_file = None

    def play_source(self, stream_link, item_information, resume_time=None):
        """Method for handling playing of sources.

        :param stream_link: Direct link of source to be played or dict containing more information about the stream
        to play
        :type stream_link: str|dict
        :param item_information: Information about the item to be played
        :type item_information:dict
        :param resume_time:Time to resume the source at
        :type resume_time:int
        :rtype:None
        """

        if not stream_link:
            g.cancel_playback()
            return

        self.item_information = item_information

        self.playing_file = stream_link
        self.mediatype = self.item_information["info"]["mediatype"]

        g.close_busy_dialog()
        g.close_all_dialogs()

        xbmcplugin.setResolvedUrl(g.PLUGIN_HANDLE, True, self._create_list_item(stream_link))

    def _create_list_item(self, stream_link):
        info = copy.deepcopy(self.item_information["info"])
        g.clean_info_keys(info)
        # g.convert_info_dates(info)

        if isinstance(stream_link, dict) and stream_link["type"] == "Adaptive":
            provider = stream_link["provider_imports"]
            provider_module = __import__(
                "{}.{}".format(provider[0], provider[1]), fromlist=[""]
                )
            if not hasattr(provider_module, "get_listitem") and hasattr(
                    provider_module, "sources"
                    ):
                provider_module = provider_module.sources()
            item = provider_module.get_listitem(stream_link)
        else:
            item = xbmcgui.ListItem(path=stream_link)
            info["FileNameAndPath"] = tools.unquote(self.playing_file)
            item.setInfo("video", info)
            item.setProperty("IsPlayable", "true")

        art = self.item_information.get("art", {})
        item.setArt(art if isinstance(art, dict) else {})
        cast = self.item_information.get("cast", [])
        item.setCast(cast if isinstance(cast, list) else [])
        item.setUniqueIDs(
            {i.split("_")[0]: info[i] for i in info if i.endswith("id")},
            )
        return item

    def onPlayBackPaused(self) -> None:
        g.log('Player failed to play')