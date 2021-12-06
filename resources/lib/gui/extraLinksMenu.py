# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.providers.media.arabseed_menu import ArabseedMenu
from resources.lib.gui.providers.sports.alostora_menu import AlostoraMenu
from resources.lib.gui.providers.sports.asgoal_menu import AsgoalMenu
from resources.lib.gui.providers.media.cimanow_menu import CimanowMenu
from resources.lib.gui.providers.media.shahed4u_menu import Shahed4uMenu
from resources.lib.gui.providers.sports.yallalive_menus import YallaliveMenu
from resources.lib.modules.globals import g
from resources.lib.modules.list_builder import ListBuilder
from resources.lib.modules.providers.handlers.extra_links import ExtraLinks


class ExtraLinksMenu:
    def __init__(self):
        self.list_builder = ListBuilder()
        self.api = ExtraLinks()

    ######################################################
    # MENUS
    ######################################################

    def extra_links(self):
        links_list = self.api.get_links()
        self.list_builder.episode_list_builder(links_list)
