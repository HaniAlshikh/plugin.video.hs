# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from bs4 import BeautifulSoup

from resources.lib.modules.globals import g
from resources.lib.modules.scrapers.request import Request

class AlbaPlayer:

    @staticmethod
    def get_sources(soup, url): # TODO: check if url can be replaced with iframe.get('src')
        sources = []
        for iframe in soup.find_all('iframe'):
            page = Request().get(iframe.get('src'), headers={'Referer': '/'.join(url.split('/')[:3])}).text
            soup = BeautifulSoup(page, 'html.parser')
            multi_link_source = soup.find(class_="albaplayer_name")

            if multi_link_source:
                sources.extend(soup.find(class_="albaplayer_name").find_all("a"))
            else:
                sources.append(iframe)
        return sources

    @staticmethod
    def get_url(source_div, url):
        channel_url = source_div.get('href') or source_div.get('src')
        g.log('AlbaPlayer: extracting source from: ' + channel_url)

        # check for other players
        if 'youtube' in channel_url:
            return channel_url

        channel_page = Request().get(channel_url, headers={'Referer': '/'.join(url.split('/')[:3])}).text
        channel_soup = BeautifulSoup(channel_page, 'html.parser')

        if channel_soup.find(class_='albaplayer_server-body'):
            video = channel_soup.find(class_='albaplayer_server-body').find('video')
            if video:
                return video.get('src').strip()

        player = channel_soup.select_one('div#player')
        if player:
            import re
            script = player.next_sibling
            encoded_link = re.search('AlbaPlayerControl\(\'(.*)\'.*', script.string).group(1)
            import base64
            try:
                g.log('attempting to decode: {}'.format(encoded_link))
                return base64.b64decode(encoded_link).decode('utf-8')
            except Exception as e:
                g.log('Faild to decode with error: {}'.format(e), 'error')

        iframe = channel_soup.find('iframe')
        if iframe:
            return iframe.get('src').strip()

        return ''
