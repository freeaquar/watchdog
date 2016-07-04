#!/usr/bin/env python
# -*- coding: utf8 -*-
from conf import conf
from topic import Topic
from newthread import NewThread


if "__main__" == __name__:
    # name = "游刃"
    # msg = "德国真的赢了"

    name = "羊女"
    msg = "羊女～申请～7月16日/周六～十渡漂流-高山划水休闲（第3期）～领队"
    data = "7.16"
    conf["watch"]["topic"] %= data

    topic = Topic()
    url = topic.obtain_url()

    nt = NewThread(url, name, msg)
    nt.auto_apply()
