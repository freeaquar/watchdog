#!/usr/bin/env python
# -*- coding: utf8 -*-
import json

from conf import conf
from util import Util


class Auth():
    def __init__(self, name, passwd):
        self.name = name
        self.passwd = passwd

    def login(self):
        content = self.login_page()

        data = {
            "formhash": Util.form_parser("id=\"formhash\".*?value=\"([^\"]+)",
                                         content),
            "referer": Util.form_parser("id=\"referer\".*?value=\"([^\"]+)",
                                        content),
            "username": self.name,
            "password": self.passwd,
            "questionid": 0,
            "answer": "",
            "cookietime": Util.form_parser(
                "id=\"cookietime\".*?value=\"([^\"]+)", content),
        }

        return data

    def login_page(self):
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        content = Util.http_get(conf["url"]["login"])
        # obj =
        # re.search('(home\.php\?mod=spacecp.*?ac=pm.*?op=checknewpm.*?rand=\w+)',
        # content);obj.group(1)

        return content


if "__main__" == __name__:
    name = u"游刃"
    auth = Auth(name, conf["info"][name])
    auth.login_page()
