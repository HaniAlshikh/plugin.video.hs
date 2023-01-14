# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import collections
from datetime import datetime

import xbmcgui

from resources.lib.common import tools
from resources.lib.database import Database
from resources.lib.modules.globals import g
from resources.lib.modules.metadata_handler import MetadataHandler

schema = {
    "info": {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("last_updated", ["TEXT", "NOT NULL", "DEFAULT '1970-01-01T00:00:00'"]),
            ]
        ),
        "table_constraints": [],
        "indices": [],
        "default_seed": [],
    },
    g.CONTENT_SHOW_GENRE: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("title", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": ["UNIQUE(title)"],
        "indices": [],
        "default_seed": [],
    },
    g.CONTENT_SHOW: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("show_genre_id", ["INTEGER", "NOT NULL"]),
                ("tvshowtitle", ["TEXT", "NOT NULL"]),
                ("info", ["PICKLE", "NULL"]),
                ("art", ["PICKLE", "NULL"]),
                ("args", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
                ("provider", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": [
            "UNIQUE(tvshowtitle)",
            "FOREIGN KEY(show_genre_id) REFERENCES " + g.CONTENT_SHOW_GENRE + "(id) DEFERRABLE INITIALLY DEFERRED",
        ],
        "default_seed": [],
    },
    g.CONTENT_SEASON: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("show_id", ["INTEGER", "NOT NULL"]),
                ("season", ["INTEGER", "NOT NULL"]),
                ("info", ["PICKLE", "NULL"]),
                ("art", ["PICKLE", "NULL"]),
                ("args", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
                ("provider", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": [
            "UNIQUE(show_id, season)",
            "FOREIGN KEY(show_id) REFERENCES " + g.CONTENT_SHOW + "(id) DEFERRABLE INITIALLY DEFERRED"
        ],
        "default_seed": [],
    },
    g.CONTENT_EPISODE: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("season_id", ["INTEGER", "NOT NULL"]),
                ("show_id", ["INTEGER", "NOT NULL"]),
                ("episode", ["INTEGER", "NOT NULL"]),
                ("info", ["PICKLE", "NULL"]),
                ("art", ["PICKLE", "NULL"]),
                ("args", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
                ("provider", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": [
            # "UNIQUE(season_id, show_id, episode)",
            "FOREIGN KEY(season_id) REFERENCES "+g.CONTENT_SEASON+"(id) DEFERRABLE INITIALLY DEFERRED",
            "FOREIGN KEY(show_id) REFERENCES "+g.CONTENT_SHOW+"(id) DEFERRABLE INITIALLY DEFERRED",
        ],
        "indices": [
            ("idx_episodes_seasonid_showid", ["season_id", "show_id"]),
        ],
        "default_seed": [],
    },
    g.CONTENT_GENRE: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("title", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": ["UNIQUE(title)"],
        "indices": [],
        "default_seed": [],
    },
    g.CONTENT_MOVIE: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("genre_id", ["INTEGER", "NOT NULL"]),
                ("info", ["PICKLE", "NULL"]),
                ("art", ["PICKLE", "NULL"]),
                ("args", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
                ("provider", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": [
            "FOREIGN KEY(genre_id) REFERENCES " + g.CONTENT_GENRE + "(id) DEFERRABLE INITIALLY DEFERRED",
        ],
        "indices": [],
        "default_seed": [],
    },
    g.CONTENT_CHANNEL_GROUP: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("title", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": ["UNIQUE(title)"],
        "default_seed": [],
    },
    g.CONTENT_CHANNEL: {
        "columns": collections.OrderedDict(
            [
                ("id", ["INTEGER", "PRIMARY KEY", "NOT NULL"]),
                ("channel_group_id", ["INTEGER", "NOT NULL"]),
                ("info", ["PICKLE", "NULL"]),
                ("art", ["PICKLE", "NULL"]),
                ("args", ["TEXT", "NOT NULL"]),
                ("url", ["TEXT", "NOT NULL"]),
                ("provider", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": [
            "FOREIGN KEY(channel_group_id) REFERENCES "+g.CONTENT_CHANNEL_GROUP+"(id) DEFERRABLE INITIALLY DEFERRED",
        ],
        "indices": [],
        "default_seed": [],
    },
}


class M3UDatabase(Database):
    def __init__(self, provider):
        super(M3UDatabase, self).__init__(g.ADDON_USERDATA_PATH + provider.name + ".db", schema)
        self.metadataHandler = MetadataHandler()
        self.page_limit = g.get_int_setting("item.limit")

    @staticmethod
    def _get_datetime_now():
        return datetime.utcnow().strftime(g.DATE_TIME_FORMAT)

    def needs_update(self):
        info = self.fetchone("SELECT * FROM info WHERE id=0")
        if not info or not info.get('last_updated'):
            return True
        return (datetime.utcnow().date() -
                tools.parse_datetime(info['last_updated'], g.DATE_TIME_FORMAT, date_only=True)
                ).days >= g.M3U_SYNC_INTERVAL

    def set_up_to_date(self):
        self.execute_sql(
            "INSERT OR REPLACE into {}(id, last_updated) VALUES(?,?)".format("info"),
            (0, self._get_datetime_now())
        )

    def re_build_database(self, silent=False):
        if not silent:
            confirm = xbmcgui.Dialog().yesno(
                g.ADDON_NAME,
                "[COLOR red]تنبيه\nسيتم مسح قاعدة البيانات بلكامل\nهل انت متأكد[/COLOR]"
            )
            if confirm == 0:
                return

        self.rebuild_database()

    def insert_show_genre(self, show_genre_id, media):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_show_genre_query,
            (
                show_genre_id,
                get(media, "title"),
                get(media, "url"),
            ),
        )

    def insert_show(self, media_id, media, show_genre_id):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_show_query,
            (
                media_id,
                show_genre_id,
                get(media, "tvshowtitle"),
                get(media, "info"),
                get(media, "art"),
                get(media, "args"),
                get(media, "url"),
                get(media, "provider"),
            ),
        )

    def insert_season(self, media_id, media, show_id):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_season_query,
            (
                media_id,
                show_id,
                get(media, "season"),
                get(media, "info"),
                get(media, "art"),
                get(media, "args"),
                get(media, "url"),
                get(media, "provider"),

            ),
        )

    def insert_episode(self, media, season_id, show_id):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_episode_query,
            (
                season_id,
                show_id,
                get(media, "episode"),
                get(media, "info"),
                get(media, "art"),
                get(media, "args"),
                get(media, "url"),
                get(media, "provider"),
            ),
        )

    def insert_genre(self, genre_id, media):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_genre_query,
            (
                genre_id,
                get(media, "title"),
                get(media, "url"),
            ),
        )

    def insert_movie(self, media, genre_id):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_movie_query,
            (
                genre_id,
                get(media, "info"),
                get(media, "art"),
                get(media, "args"),
                get(media, "url"),
                get(media, "provider"),
            ),
        )

    def insert_channel_group(self, channel_group_id, media):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_channel_group_query,
            (
                channel_group_id,
                get(media, "title"),
                get(media, "url"),
            ),
        )

    def insert_channel(self, media, channel_group_id):
        get = MetadataHandler.get_media
        return self._insert_media(
            media,
            self.upsert_channel_query,
            (
                channel_group_id,
                get(media, "info"),
                get(media, "art"),
                get(media, "args"),
                get(media, "url"),
                get(media, "provider"),
            ),
        )

    def get_categories(self, content_type):
        return self.fetchall(
            "SELECT * FROM {}".format(content_type)
        )

    def get_list(self, query):
        return self.fetchall(query)[self.page_limit * (g.PAGE - 1):self.page_limit * g.PAGE]

    def get_movies(self, genre_id):
        return self.get_list(
            "SELECT * FROM {} WHERE genre_id={}".format(g.CONTENT_MOVIE, genre_id)
        )

    def get_shows(self, show_genre_id):
        return self.get_list(
            "SELECT * FROM {} WHERE show_genre_id={}".format(g.CONTENT_SHOW, show_genre_id)
        )

    def get_seasons(self, show_id):
        return self.get_list(
            "SELECT * FROM {} WHERE show_id={}".format(g.CONTENT_SEASON, show_id)
        )

    def get_episodes(self, season_id, show_id):
        return self.get_list(
            "SELECT * FROM {} WHERE season_id={} AND show_id={}".format(g.CONTENT_EPISODE, season_id, show_id)
        )

    def get_channels(self, channel_group_id):
        return self.get_list(
            "SELECT * FROM {} WHERE channel_group_id={}".format(g.CONTENT_CHANNEL, channel_group_id)
        )

    @property
    def upsert_show_genre_query(self):
        return """
            INSERT into {}(id, title, url) 
            VALUES (?,?,?)
            """.format(g.CONTENT_SHOW_GENRE)

    @property
    def upsert_show_query(self):
        return """
            INSERT into {}(id, show_genre_id, tvshowtitle, info, art, args, url, provider) 
            VALUES (?,?,?,?,?,?,?,?)
            """.format(g.CONTENT_SHOW)

    @property
    def upsert_season_query(self):
        return """
            INSERT into {}(id, show_id, season, info, art, args, url, provider) 
            VALUES (?,?,?,?,?,?,?,?)
            """.format(g.CONTENT_SEASON)

    @property
    def upsert_episode_query(self):
        return """
            INSERT into {}(season_id, show_id, episode, info, art, args, url, provider) 
            VALUES (?,?,?,?,?,?,?,?)
            """.format(g.CONTENT_EPISODE)

    @property
    def upsert_genre_query(self):
        return """
            INSERT into {}(id, title, url) 
            VALUES (?,?,?)
            """.format(g.CONTENT_GENRE)

    @property
    def upsert_movie_query(self):
        return """
            INSERT into {}(genre_id, info, art, args, url, provider) 
            VALUES (?,?,?,?,?,?)
            """.format(g.CONTENT_MOVIE)

    @property
    def upsert_channel_group_query(self):
        return """
            INSERT into {}(id, title, url) 
            VALUES (?,?,?)
            """.format(g.CONTENT_CHANNEL_GROUP)

    @property
    def upsert_channel_query(self):
        return """
            INSERT into {}(channel_group_id, info, art, args, url, provider) 
            VALUES (?,?,?,?,?,?)
            """.format(g.CONTENT_CHANNEL)

    def _insert_media(self, media, query, data):
        if not media:
            return None
        return self.execute_sql(query, data).lastrowid
