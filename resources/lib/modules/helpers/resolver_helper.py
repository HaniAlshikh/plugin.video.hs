# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.metadata_handler import MetadataHandler
from resources.lib.modules.resolvers import Resolver


class ResolverHelper:
    """
    Helper object to stream line resolving items
    """
    @staticmethod
    def resolve_silent_or_visible(item_information, pack_select=False, overwrite_cache=False):
        """
        Method to handle automatic background or foreground resolving
        :param item_information: information on item to play
        :param pack_select: True if you want to perform a manual file selection
        :param overwrite_cache: Set to true if you wish to overwrite the current cached return value
        :return: None if unsuccessful otherwise a playable object
        """

        return Resolver().resolve_multiple_until_valid_link(item_information, pack_select, True)

    @staticmethod
    def clean_up_sources(sources: list) -> list:
        for source in sources:
            MetadataHandler.improve_source(source)
        return Resolver().cleanup_sources(sources)
