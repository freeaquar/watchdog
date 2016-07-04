#!/usr/bin/env python
# -*- coding: utf8 -*-
import re

from conf import conf
from util import Util


class NewThread(object):
    def __init__(self, page_url, name, msg):
        self.url = page_url
        self.name = name
        self.msg = msg

        print "init the newthread"

    def auto_apply(self):
        url, content = self._distinct()
        if url:
            self._apply(url, content)
        else:
            print "already succ"

    def _distinct(self):
        content = Util.http_get(self.url)

        pattern = "id=\"fastpostform\".*?action=\"([^\"]+)"
        obj = re.search(pattern, content)

        if obj:
            return (conf["url"]["domain"] + Util.url_format(obj.group(1)),
                    content)

    def _apply(self, url, content):
        max_retry = 3
        pattern = "name=\"%s\".*?value=\"([^\"]+)"
        data = {
            "message": self.msg,
            "posttime": Util.form_parser(pattern % "posttime", content),
            "formhash": Util.form_parser(pattern % "formhash", content),
            "sesig": Util.form_parser(pattern % "usesig", content),
            "subject": Util.form_parser(pattern % "subject", content),
        }

        while max_retry:
            try:
                print "try to submit comment"
                content = Util.http_post(url, data)
                print "submit succ"
                break
            except:
                max_retry -= 1
                print "failed %s" % max_retry


if "__main__" == __name__:
    name = "游刃"
    msg = "德国真的赢了"

    # topic = Topic()
    # print topic.obtain_url()

    url = "http://bbs.clctrip.com/forum.php?mod=viewthread&tid=49&extra=page%3D1"

    nt = NewThread(url, name, msg)
    nt.auto_apply()
