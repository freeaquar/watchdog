#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time

from util import url_trim, Recorder


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

            Recorder.info(self, self._user, "init")

        except Exception as e:
            Recorder.error(self, self._user, "init failed", e)
            raise Exception(e)

    def locate_post_url(self):
        while True:
            url = self._locate()
            if not url:
                msg = "mismatch and sleep for {}".format(self._interval)
                Recorder.debug(self, self._user, msg)

                time.sleep(self._interval)
                continue

            msg = "hit the pattern: {}".format(url)
            Recorder.info(self, self._user, msg)

            return url

    def _locate(self):
        try:
            r = self._session.get(self._page_url)
            url = (
                self._domain + re.search(self._post_regex, r.text).group(1)
            )

            return url_trim(url)

        except IndexError as e:
            pass
        except Exception as e:
            Recorder.error(self, self._user, "_run failed", e)

        return False

    def __repr__(self):
        return "<Topic>"
