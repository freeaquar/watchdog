#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from util import url_trim, Recorder


class Post(object):
    """ try to get the topic url by pattern """
    def __init__(self, session, user, config, post_url):
        try:
            self._session = session
            self._user = user

            self._page_url = post_url
            self._domain = config["domain"]

            self._name = config["name"]
            self._msg = config["msg"]
            self._max_retry = config["post_max_retry"]

            self._reply_args_regex = config["post_reply_args_regex"]
            self._reply_url_regex = config["post_reply_url_regex"]

            Recorder.info(self, self._user, "init")
        except Exception as e:
            Recorder.error(self, self._user, "init failed", e)
            raise Exception(e)

    def reply(self):
        self._get_text()
        self._reply()

    def _get_text(self):
        while True:
            try:
                r = self._session.get(self._page_url)
                r.raise_for_status()

                self._text = r.text
                return
            except Exception as e:
                Recorder.error(self, self._user, "_get_text failed", e)

    def _reply(self):
        url = self._get_reply_url()
        data = {
            "message": self._msg,
            "posttime": self._get_args("posttime"),
            "formhash": self._get_args("formhash"),
            "sesig": self._get_args("usesig"),
            "subject": self._get_args("subject"),
        }

        # if the self._msg is exist in the page, do nothing
        if self._exist():
            Recorder.info(self, self._user, "reply exist already")
            return

        while self._max_retry:
            try:
                Recorder.debug(self, self._user, "try to submit comment")

                r = self._session.post(url, data=data)
                r.raise_for_status()

                Recorder.info(self, self._user, "submit succ")
                break
            except Exception as e:
                msg = "_reply failed[{}]".format(self._max_retry)
                Recorder.warn(self, self._user, msg, e)
        else:
            Recorder.error(self, self._user, "run out of reply request retries")

    def _get_reply_url(self):
        uri = re.search(self._reply_url_regex, self._text).group(1)
        return self._domain + url_trim(uri)

    def _get_args(self, name):
        return (re.search(self._reply_args_regex.format(name), self._text)
                .group(1))

    def _exist(self):
        if self._msg in self._text:
            return True

        return False

    def __repr__(self):
        return "<Post>"
