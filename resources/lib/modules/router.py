# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import json

import xbmc
import xbmcgui
from xbmc import sleep

from resources.lib.modules.globals import g
from resources.lib.modules.helpers.player_helper import PlayerHelper


def dispatch(params):
    # params = g.REQUEST_PARAMS
    action = params.get("action")
    action_args = params.get("action_args")
    link = params.get('link')
    pack_select = params.get("packSelect")
    source_select = params.get("source_select") == "true"
    overwrite_cache = params.get("seren_reload") == "true"
    resume = params.get("resume")
    force_resume_check = params.get("forceresumecheck") == "true"
    force_resume_off = params.get("forceresumeoff") == "true"
    force_resume_on = params.get("forceresumeon") == "true"
    smart_url_arg = params.get("smartPlay") == "true"
    mediatype = params.get("mediatype")
    category = params.get("category")

    g.log("HS, Running Path - {}".format(g.REQUEST_PARAMS))

    if action is None:
        from resources.lib.gui import homeMenu
        homeMenu.Menus().home()

    elif action == "providersHome":
        from resources.lib.gui.providersMenus import Menus
        Menus().providers()

    elif action == "providerMenu":
        from resources.lib.gui.providersMenus import Menus
        Menus().provider_menu(action_args["provider"])

    elif action == "movies":
        from resources.lib.gui.providersMenus import Menus
        Menus().PROVIDERS[action_args["provider"]].movies(category)

    elif action == "shows":
        from resources.lib.gui.providersMenus import Menus
        Menus().PROVIDERS[action_args["provider"]].shows(category)

    elif action == "showSeasons":
        from resources.lib.gui.providersMenus import Menus
        Menus().PROVIDERS[action_args["provider"]].show_seasons(action_args["url"])

    elif action == "seasonEpisodes":
        from resources.lib.gui.providersMenus import Menus
        Menus().PROVIDERS[action_args["provider"]].episodes(action_args["url"])

    elif action == "search":
        mediatypes = {'فلم': g.MEDIA_MOVIE, 'مسلسل': g.MEDIA_SHOW}
        mediatype = xbmcgui.Dialog().select(
            "{}: {}".format(g.ADDON_NAME, 'بحث عن'), [*mediatypes.keys()]
        )
        if mediatype == -1: return
        query = g.get_keyboard_input('البحث')
        from resources.lib.gui.providersMenus import Menus
        Menus().PROVIDERS[action_args["provider"]].search(query, [*mediatypes.values()][mediatype])

    elif action == "getSources":
        sources = action_args.get('sources')
        if sources is None:  # empty array means we already tested all sources
            from resources.lib.gui.providersMenus import Menus
            sources = Menus().PROVIDERS[action_args["provider"]].sources(action_args["url"])
            from resources.lib.modules.helpers.resolver_helper import ResolverHelper
            action_args['sources'] = ResolverHelper().clean_up_sources(sources)
            g.log('found sources: ' + str(action_args['sources']))

        PlayerHelper.ensure_all_sources_were_tried(action_args)

    elif action == "authRealDebrid":
        from resources.lib.debrid import real_debrid

        real_debrid.RealDebrid().auth()
