# -*- coding: utf-8 -*-

from resources.lib.modules.globals import g


class HomeMenus:

    @staticmethod
    def home():
        g.add_directory_item('افلام ومسلسلات',
                             action='mediaProvidersHome',
                             description='قائمة المواقع المدعومة لمشاهدة احدث الافلام والمسلسلات العربية')
        g.add_directory_item('رياضة',
                             action='sportsProvidersHome',
                             description='قائمة المواقع المدعومة لمشاهدة اخر الاحداث الرياضية')
        g.add_directory_item(g.get_language_string(30013),
                             action='searchMenu',
                             description=g.get_language_string(30397))
        # g.add_directory_item(g.get_language_string(30027),
        #                      action='toolsMenu',
        #                      description=g.get_language_string(30398))
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def search_menu():
        # if g.get_bool_setting('searchHistory'):
        #     g.add_directory_item(g.get_language_string(30025),
        #                          action='moviesSearchHistory',
        #                          description=g.get_language_string(30401))
        #     g.add_directory_item(g.get_language_string(30026),
        #                          action='showsSearchHistory',
        #                          description=g.get_language_string(30402))
        # else:
        g.add_directory_item(g.get_language_string(30025),
                             action='searchMovies',
                             description=g.get_language_string(30399))
        g.add_directory_item(g.get_language_string(30026),
                             action='searchShows',
                             description=g.get_language_string(30400))
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def tools_menu():
        g.add_directory_item(g.get_language_string(30037),
                             action='providerTools',
                             description=g.get_language_string(30405))
        if g.debrid_available():
            g.add_directory_item(g.get_language_string(30038),
                                 action='debridServices',
                                 description=g.get_language_string(30406))
        g.add_directory_item(g.get_language_string(30028),
                             action='clearCache',
                             is_folder=False,
                             description=g.get_language_string(30407))
        g.add_directory_item(g.get_language_string(30039),
                             action='clearTorrentCache',
                             is_folder=False,
                             description=g.get_language_string(30408))
        g.add_directory_item(g.get_language_string(30199),
                             action='clearSearchHistory',
                             is_folder=False,
                             description=g.get_language_string(30409))
        g.add_directory_item(g.get_language_string(30040),
                             action='openSettings',
                             is_folder=False,
                             description=g.get_language_string(30410))
        g.add_directory_item(g.get_language_string(30041),
                             action='cleanInstall',
                             is_folder=False,
                             description=g.get_language_string(30411))
        g.add_directory_item(g.get_language_string(30234),
                             action='traktSyncTools',
                             is_folder=True,
                             description=g.get_language_string(30412))
        g.add_directory_item('Download Manager',
                             action='downloadManagerView',
                             is_folder=False,
                             description='View Current Downloads')
        if g.get_bool_setting("skin.testmenu", False):
            g.add_directory_item('Window Tests',
                                 action='testWindows',
                                 description=g.get_language_string(30413))
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def provider_menu():
        g.add_directory_item(g.get_language_string(30149),
                             action='manualProviderUpdate',
                             is_folder=False,
                             description=g.get_language_string(30414))
        g.add_directory_item(g.get_language_string(30150),
                             action='manageProviders',
                             is_folder=False,
                             description=g.get_language_string(30415))
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def test_windows():
        g.add_directory_item(g.get_language_string(30492),
                             action='testPlayingNext',
                             is_folder=False,
                             description=g.get_language_string(30419))
        g.add_directory_item(g.get_language_string(30493),
                             action='testStillWatching',
                             is_folder=False,
                             description=g.get_language_string(30420))
        g.add_directory_item(g.get_language_string(30494),
                             action='testResolverWindow',
                             is_folder=False,
                             description=g.get_language_string(30421))
        g.add_directory_item(g.get_language_string(30495),
                             action='testSourceSelectWindow',
                             is_folder=False,
                             description=g.get_language_string(30422))
        g.add_directory_item(g.get_language_string(30496),
                             action='testManualCacheWindow',
                             is_folder=False,
                             description=g.get_language_string(30490))
        g.close_directory(g.CONTENT_FOLDER)
