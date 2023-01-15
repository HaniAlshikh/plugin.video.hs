# -*- coding: utf-8 -*-

from resources.lib.modules.globals import g


class HomeMenus:

    @staticmethod
    def home():
        g.add_directory_item('افلام، مسلسلات، وقنوات',
                             action='mediaProvidersHome',
                             description='قائمة المواقع المدعومة لمشاهدة احدث الافلام، المسلسلات، والقنوات العربية')
        g.add_directory_item('رياضة',
                             action='sportsProvidersHome',
                             description='قائمة المواقع المدعومة لمشاهدة اخر الاحداث الرياضية')
        g.add_directory_item('روابط اضافية',
                             action='extraLinksMenu',
                             description='قائمة من الروابط الاضافية بناء على ملف بصيغة json',
                             menu_item={'art': {"thumb": g.DEFAULT_FANART}})
        g.add_directory_item(g.get_language_string(30013),
                             action='searchMenu',
                             description=g.get_language_string(30397))
        g.add_directory_item(g.get_language_string(30027),
                             action='toolsMenu',
                             description=g.get_language_string(30398))
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
                             action='searchMoviesGlobally',
                             description=g.get_language_string(30399))
        g.add_directory_item(g.get_language_string(30026),
                             action='searchShowsGlobally',
                             description=g.get_language_string(30400))
        g.add_directory_item("البحث في القنوات...",
                             action='searchChannelsGlobally',
                             description='ابحث عن القنوات بالعنوان')
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def tools_menu():
        g.add_directory_item('ادوات موفري المصادر',
                             action='providerTools',
                             description=g.get_language_string(30405))
        g.close_directory(g.CONTENT_FOLDER)

    @staticmethod
    def provider_menu():
        g.add_directory_item(g.get_language_string(30149),
                             action='manualProviderUpdate',
                             is_folder=False,
                             description=g.get_language_string(30414))
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
