# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.common.exceptions import RunNotNeeded
from resources.lib.modules.globals import g
from resources.lib.modules.providers.media.media_provider import MediaProvider
from resources.lib.database.m3u import M3UDatabase


class MagicHD(MediaProvider):
    def __init__(self):
        super().__init__(
            'ماجيك HD',
            "magichd",
            [g.get_setting('general.magicHD')],
        )
        self.db = M3UDatabase(self)

    def get_movies_categories(self) -> list:
        return self._get_categories(g.CONTENT_GENRE)

    def get_movies_list(self, category: str) -> list:
        return self.db.get_movies(category)

    def get_shows_categories(self) -> list:
        return self._get_categories(g.CONTENT_SHOW_GENRE)

    def get_shows_list(self, url: str) -> list:
        return self.db.get_shows(url)

    def get_shows_seasons(self, url: str) -> list:
        return self.db.get_seasons(url)

    def get_season_episodes(self, url: str) -> list:
        url = url.split("-")
        return self.db.get_episodes(url[0], url[1])

    def get_channels_categories(self) -> list:
        return self._get_categories(g.CONTENT_CHANNEL_GROUP)

    def get_channels_list(self, category: str) -> list:
        return self.db.get_channels(category)

    def search(self, query: str, mediatype: str) -> list:
        # TODO: auramod onscreen keyboard by Cartmandos (Titan Bingie) arabic fix
        return self.db.search(query, mediatype+"s")

    def get_sources(self, url: str) -> list:
        return [
            self._get_source_meta(
                display_name=self.display_name,
                url=url,
                quality="HD",
                type="hoster",
                provider=self.name,
            )
        ]

    def sync(self, silent: bool = False, force: bool = False):
        self.progress_dialog = g.progress_notification(self.notification_header, "جاري مزامنة القنوات", silent)
        g.log("Starting {} sync: {}".format(self.name, self.urls[0]))
        try:
            if len(self.urls) == 0:
                self.progress_dialog.update(100, self.notification_header, 'تعذر المزامنة: يرجى تحديد المصدر في الاعدادات')
                g.log("No link to sync...")
                raise RunNotNeeded()
            if not force and not self.db.needs_update():
                self.progress_dialog.update(100, self.notification_header, 'قاعدة البيانات محدثة')
                g.log("database is up to date. Abort syncing...")
                raise RunNotNeeded()

            from resources.lib.modules.global_lock import GlobalLock
            with GlobalLock(self.__class__.__name__, False):
                self._sync()
        except Exception as e:
            g.log("finished syncing: {}".format(e))
        self.progress_dialog.close()

    ###################################################
    # HELPERS
    ###################################################

    def _get_categories(self, content_type: str):
        return self.db.get_categories(content_type)

    def _sync(self):
        parser = self._extract_m3u()
        media_list = parser.get_list()
        g.log("downloaded {} m3u entries".format(len(media_list)))
        if len(media_list) == 0:
            self.progress_dialog.update(100, self.notification_header, "تعذر المزامنة: يرجى التحقق من الرابط في الاعدادات")
            g.log("Failed to sync {} db: {}".format(self.name, self.urls[0]), "warning")
            return

        self.db.re_build_database(silent=True)
        show_genre_id = show_id = season_id = episode_id = genre_id = movie_id = channel_group_id = channel_id = 1  # don't change to 0
        show_genres_dict = shows_dict = seasons_dict = genres_dict = channels_dict = {}
        import re
        from resources.lib.common import tools
        for i, media in enumerate(media_list):
            p = int(100 * float(i)/float(len(media_list)))
            self.progress_dialog.update(p, self.notification_header, media['name'])
            try:
                episode = re.search('.*(S\d\d\sE\d\d).*', media['name'])
                if episode:
                    current_show_genre_id = show_genres_dict.get(media.get('category')) or show_genre_id
                    if not show_genres_dict.get(media.get('category')):
                        self.db.insert_show_genre(
                            current_show_genre_id, self._extract_m3u_meta(
                            media, g.MEDIA_FOLDER,
                            poster="",
                            title=media['category'],
                            url=current_show_genre_id
                            )
                        )
                        show_genres_dict[media.get('category')] = current_show_genre_id
                        show_genre_id += 1

                    show_title = media.get('name').replace(episode.group(1), "").strip()
                    current_show_id = shows_dict.get(show_title) or show_id
                    if not shows_dict.get(show_title):
                        self.db.insert_show(current_show_id, self._extract_m3u_meta(
                            media, g.MEDIA_SHOW,
                            tvshowtitle=show_title,
                            title=show_title,
                            url=current_show_id
                            ),
                            current_show_genre_id,
                        )
                        shows_dict[show_title] = current_show_id
                        show_id += 1

                    episode = episode.group(1).split()  # "S01 E03"

                    season_title = "{} {}".format(show_title, episode[0][1:])
                    current_season_id = seasons_dict.get(season_title) or season_id
                    if not seasons_dict.get(season_title):
                        self.db.insert_season(current_season_id, self._extract_m3u_meta(
                            media, g.MEDIA_SEASON,
                            title=episode[0][1:],
                            season=int(episode[0][1:]),
                            url="{}-{}".format(current_season_id, current_show_id)
                            ),
                            current_show_id
                        )
                        seasons_dict[season_title] = current_season_id
                        season_id += 1

                    self.db.insert_episode(self._extract_m3u_meta(
                        media, g.MEDIA_EPISODE,
                        title=episode[1][1:],
                        tvshowtitle=show_title,
                        episode=int(episode[1][1:]),
                        season=int(episode[0][1:]),
                        url=media['url'],
                        ),
                        current_season_id,
                        current_show_id,
                    )

                elif media['url'].endswith(tools.get_supported_media("video")):
                    current_genre_id = genres_dict.get(media.get('category')) or genre_id
                    if not genres_dict.get(media.get('category')):
                        self.db.insert_genre(current_genre_id, self._extract_m3u_meta(
                            media, g.MEDIA_FOLDER,
                            poster="",
                            title=media['category'],
                            url=current_genre_id
                            )
                        )
                        genres_dict[media.get('category')] = current_genre_id
                        genre_id += 1

                    self.db.insert_movie(self._extract_m3u_meta(
                        media, g.MEDIA_MOVIE,
                        category=media['category'],
                        url=media['url'],
                        ),
                        current_genre_id
                    )

                else:
                    current_channel_group_id = channels_dict.get(media.get('category')) or channel_group_id
                    if not channels_dict.get(media.get('category')):
                        self.db.insert_channel_group(current_channel_group_id, self._extract_m3u_meta(
                            media, g.MEDIA_FOLDER,
                            poster="",
                            title=media['category'],
                            url=current_channel_group_id
                            )
                        )
                        channels_dict[media.get('category')] = current_channel_group_id
                        channel_group_id += 1

                    self.db.insert_channel(self._extract_m3u_meta(
                        media, g.MEDIA_CHANNEL,
                        category=media['category'],
                        url=media['url'],
                        ),
                        current_channel_group_id
                    )
            except Exception as e:
                g.log("Failed to insert: {}\n{}".format(e, media), "warning")
                # raise e

        g.log("Finished inserting")
        g.log("Creating PVR source...")
        parser.remove_by_extension('mp4')
        pvr_file = g.M3U_FILES_PATH+"/"+self.name+".m3u"
        parser.to_file(g.M3U_FILES_PATH+"/"+self.name+".m3u", format="m3u")
        g.log("PVR source saved to: {}".format(pvr_file))

        self.db.set_up_to_date()
        self.progress_dialog.update(100, self.notification_header, 'تمت الزامنة')