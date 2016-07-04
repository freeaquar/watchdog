#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests
import codecs
import json
import re


class Util(object):
    cks = None

    @classmethod
    def http_get(cls, url):
        r = requests.get(url, cookies=Util._cookies())

        return Util._respons(r)

    @classmethod
    def http_post(cls, url, data):
        r = requests.post(url, cookies=Util._cookies(), data=data)

        return Util._respons(r)

    @classmethod
    def url_format(cls, url):
        return url.replace("&amp;", "&")

    @classmethod
    def form_parser(cls, pattern, content):
        """ get HTML form's field """
        obj = re.search(pattern, content)

        if obj:
            return obj.group(1)
        else:
            raise

    @classmethod
    def _respons(cls, r):
        if r.status_code != 200:
            return False

        Util._refresh_cookies(r.cookies)

        return r.content

    @classmethod
    def _cookies(cls):
        if not Util.cks:
            with codecs.open("cookies.txt", "r", "utf-8") as f:
                info = f.read()

            Util.cks = json.loads(info)

        return Util.cks

    @classmethod
    def _refresh_cookies(cls, cookies):
        for i, v in cookies.items():
            Util.cks[i] = v

        # cover the old cookies file
        with codecs.open("cookies.txt", "w", "utf-8") as f:
            f.write(json.dumps(Util.cks))


if "__main__" == __name__:
    pass
