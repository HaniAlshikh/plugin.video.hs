# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.common.tools import fix_arabic
from resources.lib.modules.globals import g
from resources.lib.modules.helpers.player_helper import PlayerHelper


def dispatch(params):
    # params = g.REQUEST_PARAMS
    action = params.get("action")
    action_args = params.get("action_args") or {}
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

    ######################################################
    # HOME
    ######################################################

    if action is None:
        from resources.lib.gui.homeMenu import HomeMenus
        HomeMenus().home()

    elif action == "mediaProvidersHome":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().media_providers()

    elif action == "sportsProvidersHome":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().sports_providers()

    ######################################################
    # MENUS
    ######################################################

    elif action == "mediaProviderMenu":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().media_provider_menu(action_args["provider"])

    elif action == "extraLinksMenu":
        from resources.lib.gui.extraLinksMenu import ExtraLinksMenu
        ExtraLinksMenu().extra_links()

    elif action == "searchMenu":
        from resources.lib.gui.homeMenu import HomeMenus
        HomeMenus().search_menu()

    elif action == "toolsMenu":
        from resources.lib.gui.homeMenu import HomeMenus
        HomeMenus().tools_menu()

    elif action == "providerTools":
        from resources.lib.gui.homeMenu import HomeMenus
        HomeMenus().provider_menu()

    ######################################################
    # PROVIDERS
    ######################################################

    elif action == "movies":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().PROVIDERS[action_args["provider"]].movies(category)

    elif action == "shows":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().PROVIDERS[action_args["provider"]].shows(category)

    elif action == "channels":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().PROVIDERS[action_args["provider"]].channels(category)

    elif action == "showSeasons":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().PROVIDERS[action_args["provider"]].show_seasons(action_args["url"])

    elif action == "seasonEpisodes":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().PROVIDERS[action_args["provider"]].episodes(action_args["url"])

    elif action == "games":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().PROVIDERS[action_args["provider"]].games()

    ######################################################
    # SOURCES
    ######################################################

    elif action == "getSources":
        sources = action_args.get('sources')
        if sources is None:  # empty array means we already tested all sources
            from resources.lib.gui.providersMenus import ProviderMenus
            sources = ProviderMenus().PROVIDERS[action_args["provider"]].sources(action_args["url"])
            from resources.lib.modules.helpers.resolver_helper import ResolverHelper
            action_args['sources'] = ResolverHelper().clean_up_sources(sources)
            g.log('found sources: ' + str(action_args['sources']))

        if source_select:
            options = {"{} {}".format(s['display_name'], s.get('channel', "")): s for s in sources}
            action_args['sources'] = [g.get_option_input(options=options)]
            if not action_args['sources'][0]: return

        PlayerHelper.ensure_all_sources_were_tried(action_args)

    elif action == "syncM3U":
        from resources.lib.modules.providers.media.MagicHD import MagicHD
        MagicHD().sync(force=action_args.get('force'))

    ######################################################
    # SEARCH
    ######################################################

    elif action == "search":
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().search(provider=action_args['provider'])

    elif action == "searchMovies" or action == "searchShows" or action == "searchChannels":
        mediatype = g.MEDIA_MOVIE if action == "searchMovies" else g.MEDIA_SHOW if action == "searchShows" else g.MEDIA_CHANNEL
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().search(fix_arabic(params.get('query')), mediatype, params.get('provider'))

    elif action == "searchMoviesGlobally" or action == "searchShowsGlobally" or action == "searchChannelsGlobally":
        mediatype = g.MEDIA_MOVIE if action == "searchMoviesGlobally" else g.MEDIA_SHOW if action == "searchShowsGlobally" else g.MEDIA_CHANNEL
        from resources.lib.gui.providersMenus import ProviderMenus
        ProviderMenus().search(mediatype=mediatype)

    ######################################################
    # TOOLS
    ######################################################

    elif action == "manualProviderUpdate":
        g.execute('RunPlugin("plugin://plugin.video.hs/?action=syncM3U&action_args={}")'.format(g.create_args({'force': True})))

    ######################################################
    # SERVICES
    ######################################################

    elif action == "authRealDebrid":
        from resources.lib.debrid import real_debrid
        real_debrid.RealDebrid().auth()