import re


def m3u2list(data):
    response = data + "#EXT#"
    matches = re.compile('(?s)^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)#EXT#', re.M).findall(
        response.replace('#EXTINF', '#EXT#\n#EXTINF'))
    li = []
    for params, display_name, uri in matches:
        url = uri
        if uri.startswith('#'):
            for ln in uri.splitlines():
                if not ln.startswith('#'):
                    url = ln
                else:
                    if ln.startswith('#EXTGRP'):
                        params += ln.replace('"', '').replace("#EXTGRP:", ' group_title="') + '"'

        item_data = {"params": params, "display_name": display_name.strip(), "url": url.strip()}
        li.append(item_data)
    ch_list = []
    for channel in li:
        item_data = {"display_name": (channel["display_name"].decode("utf-8", "ignore")), "url": channel["url"]}
        matches = re.compile(' (.*?)="(.*?)"').findall(channel["params"])
        for field, value in matches:
            item_data[field.strip().lower()] = value.strip()
        ch_list.append(item_data)
    return ch_list
