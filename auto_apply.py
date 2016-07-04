#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests
import codecs
import time
import json
import re


class Topic(object):
    def __init__(self):
        self.sleep = 1

        self.filtered_words = []
        self.cookies = {}
        self.domain = "http://bbs.clctrip.com/"
        self.url = self.domain + "forum.php?mod=forumdisplay&fid=2"

        self._org_filtered_words()
        self._org_cookie()

    def obtain_url(self):
        while True:
            uri = self._run()
            if uri:
                break

        return self.domain + uri

    def _run(self):
        r = requests.get(self.url, cookies=self.cookies)
        for i, v in r.cookies.items():
            self.cookies[i] = v

        pattern = "<a href=\"([^\"]*).*?7\.9/7\.10.*?一日.*?休闲"
        obj = re.search(pattern, r.content)

        if obj:
            return obj.group(1).replace("&amp;", "&")

        time.sleep(self.sleep)
        return False

    def _org_filtered_words(self):
        with codecs.open("filtered_words.txt", "r", "utf-8") as f:
            lines = f.readlines()
            for line in lines:
                self.filtered_words.append(line.strip())

    def _org_cookie(self):
        cookies = {
            "x36W_2132_saltkey": "DoTww8sS",
            "x36W_2132_lastvisit": "1467017025",
            "x36W_2132_seccode": "46.16d6a6a9c40a93c7f8",
            "x36W_2132_ulastactivity": "1c1fp8gM1r6XcBeP18O2B2%2FX%2F4xUPGX1LOZZ5LNYXGWC9psC77Qb",
            "x36W_2132_auth": "4b38XTQS8eZJ6VMR1GkiVXxe3AavTfDB2J6vHjjqj7t2u1QjNXnoJo4TaG9X81hVv%2FMRP373c%2BodNWU81ixquw",
            "x36W_2132_lastcheckfeed": "73%7C1467020631",
            "x36W_2132_security_cookiereport": "7074%2BTci3xdMbPULh3WzaNZaP7JUeY2s8OTaaSWve4sRBaYMLXbn",
            "x36W_2132_visitedfid": "2",
            "x36W_2132_checkpm": "1",
            "x36W_2132_sendmail": "1",
            "x36W_2132_smile": "1D1",

            # set-cookies
            "x36W_2132_lastact": "1467034557%09forum.php%09forumdisplay",
            "x36W_2132_st_t": "73%7C1467034557%7Cef07b7d66a69d82d54e90104b26f8a59",
            "x36W_2132_forum_lastvisit": "D_2_1467034557",
            "x36W_2132_sid": "TYZWY1",
        }

        self.cookies = cookies


class NewThread(object):
    def __init__(self, page_url, name, msg):
        self.url = page_url
        self.name = name
        self.msg = msg

    def auto_apply(self):
        url, content = self._distinct()
        if url:
            self._apply(url, content)
        else:
            print "already succ"

    def _distinct(self):
        content = Util.http_get(self.url)

        cnt = content.count(self.name)
        if cnt > 2:
            return "", ""

        pattern = "id=\"fastpostform\".*?action=\"([^\"]+)"
        obj = re.search(pattern, content)

        if obj:
            return Util.url_format(obj.group(1)), content

    def _apply(self, url, content):
        def _parser(pattern):
            obj = re.search(pattern, content)

            if obj:
                return obj.group(1)
            else:
                raise

        max_retry = 3
        data = {
            "message": self.msg,
            "posttime": _parser("id=\"posttime\" value=\"([^\"]+)"),
            "formhash": _parser("name=\"formhash\" value=\"([^\"]+)"),
            "sesig": _parser("name=\"usesig\" value=\"([^\"]+)"),
            "subject": _parser("name=\"subject\" value=\"([^\"]+)"),
        }

        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        while max_retry:
            try:
                content = Util.http_post(url, data)

                break
            except:
                max_retry -= 1
                print "failed"
        else:
            print "finally succ"


class Util(object):
    cks = None
    domain = "http://bbs.clctrip.com/"

    @classmethod
    def http_get(cls, url):
        r = requests.get(url, cookies=Util._cookies())

        return Util._respons(r)

    @classmethod
    def http_post(cls, url, data):
        r = requests.post(url, cookies=Util._cookies(), data=data)

        return Util._respons(r)

    @classmethod
    def _respons(cls, r):
        if r.status_code != 200:
            return False

        Util._refresh_cookies(r.cookies)

        return r.content

    @classmethod
    def url_format(cls, match_url):
        return cls.domain + match_url.replace("&amp;", "&")

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
    name = "游刃"
    msg = "希望德国加油吧"

    # topic = Topic()
    # print topic.obtain_url()

    url = "http://bbs.clctrip.com/forum.php?mod=viewthread&tid=49&extra=page%3D1"

    nt = NewThread(url, name, msg)
    nt.auto_apply()
