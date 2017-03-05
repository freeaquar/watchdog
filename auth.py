#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from util import Recorder


class Auth(object):
    """Try to login automatically.
    return False if something wrong
    else the login info will be store in the session
    """

    def __init__(self, session, user, config):
        try:
            self._session = session
            self._user = user

            self._name = config["name"]
            self._passwd = config["passwd"]

            self._page_url = config["login_page_url"]
            self._submit_url = config["login_submit_url"]
            self._referer_url = config["login_referer_url"]
            self._succ_flag = config["login_succ_flag"]

            self._formhash_regex = config["formhash_regex"]

            Recorder.info(self, self._user, "init")

        except Exception as e:
            Recorder.error(self, self._user, "init failed", e)
            raise Exception(e)

    def confirm(self):
        try:
            r = self._session.get(self._page_url)
            data = {
                "formhash": (re.search(self._formhash_regex, r.text).group(1)),
                "referer": self._referer_url,
                "loginfield": "username",
                "username": self._name,
                "password": self._passwd,
                "questionid": 0,
                "answer": '',
                "cookietime": 2592000,
            }
            r = self._session.post(self._submit_url, data=data)

            # check if login successed
            # XXX can't handle Verification Code
            if self._succ_flag not in r.text:
                raise Exception("mismatch key words in the page")

            Recorder.info(self, self._user, "confirm succ")
        except Exception as e:
            Recorder.error(self, self._user, "confirm failed", e)
            raise Exception(e)

    def __repr__(self):
        return "<Auth>"
