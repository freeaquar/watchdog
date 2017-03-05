#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from util import url_trim


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

            print "{}:{} init the post".format(self, self._user)
        except Exception as e:
            print "{}:{} init err: {}|{}".format(self, self._user, type(e),
                                                 str(e))
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
                print "{}:{} _get_text err: {}|{}".format(self, self._user,
                                                          type(e), str(e))

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
            print "{}:{} reply exist already".format(self, self._user)
            return

        while self._max_retry:
            try:
                print "{}:{} try to submit comment".format(self, self._user)

                r = self._session.post(url, data=data)
                r.raise_for_status()

                print "{}:{} submit succ".format(self, self._user)
                break
            except Exception as e:
                self._max_retry -= 1
                print "{}:{} _reply err {} {}|{}".format(
                    self, self._name, self._max_retry, type(e), str(e)
                )

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
