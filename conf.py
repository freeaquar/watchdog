#!/usr/bin/env python
# -*- coding: utf8 -*-
conf = {}


# for watcher
conf["interval"] = 0.5
conf["info"] = {
    "游刃": "ICANPLAY",
    "羊女": "123456",
}

conf["pub"] = {}
# conf["pub"]["logs"] = True
conf["pub"]["cookies"] = True  # save to file while True
conf["pub"]["domain"] = "http://bbs.clctrip.com/"  # save to file while True


# url
conf["url"] = {}
conf["url"]["domain"] = "http://bbs.clctrip.com/"
conf["url"]["login"] = conf["url"]["domain"] + "member.php?mod=logging&action=login"
conf["url"]["topic"] = conf["url"]["domain"] + "forum.php?mod=forumdisplay&fid=2"
conf["url"]["newthread"] = conf["url"]["domain"] + "forum.php"


# watch special one
conf["watch"] = {}
conf["watch"]["board"] = "短线旅行认领"
conf["watch"]["topic"] = "<a href=\"([^\"]*).*?%s.*?一日.*?休闲"
