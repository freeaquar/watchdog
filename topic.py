#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time

from util import url_trim


class Topic(object):
    """ try to get the topic url by pattern """

    def __init__(self, session, user, config):
        try:
            self._session = session
            self._user = user

            self._domain = config["domain"]
            self._page_url = config["topic_page_url"]
            self._interval = config["topic_interval"]

            self._post_regex = config["post_regex"]

            print "{}:{} init the topic".format(self, self._user)

        except Exception as e:
            print "{}:{} init err: {}|{}".format(self, self._user, type(e),
                                                 str(e))
            raise Exception(e)

    def process(self):
        while True:
            url = self._run()
            if not url:
                print ("{}:{} didn't hit the pattern and sleep for: {}s"
                       .format(self, self._user, self._interval))
                time.sleep(self._interval)
                continue

            print "{}:{} hit the pattern: {}".format(self, self._user, url)
            return url

    def _run(self):
        try:
            r = self._session.get(self._page_url)
            url = (
                self._domain + re.search(self._post_regex, r.text).group(1)
            )

            return url_trim(url)

        except IndexError as e:
            pass
        except Exception as e:
            print "{}:{} _run err: {}|{}".format(self, self._user, type(e),
                                                 str(e))
        return False

    def __repr__(self):
        return "<Topic>"
