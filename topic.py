#!/usr/bin/env python
# -*- coding: utf8 -*-
import time
import re

from conf import conf
from util import Util


class Topic(object):
    """ try to get the topic'url with pattern """

    def __init__(self):
        self.url = self.topic_url()

        print "ready to watch..."

    def topic_url(self):
        # content = Util.http_get(conf["url"]["topic"])
        # re.search()
        # XXX not finished
        return "http://bbs.clctrip.com/forum.php?mod=forumdisplay&fid=2"

    def obtain_url(self):
        while True:
            url = self._run()
            if url:
                print "hit the pattern: %s" % url
                return url

            print "didn't hit the pattern and sleep for: %ss" % conf["interval"]
            time.sleep(conf["interval"])

    def _run(self):
        content = Util.http_get(self.url)

        obj = re.search(conf["watch"]["topic"], content)

        if obj:
            return Util.url_format(conf["url"]["domain"] + obj.group(1))

        return False


if "__main__" == __name__:
    topic = Topic()
    print topic.obtain_url()
