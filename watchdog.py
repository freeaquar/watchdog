#!/usr/bin/env python
# -*- coding: utf8 -*-

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import requests
import configparser

from auth import Auth
from topic import Topic
from post import Post


class WatchDog(object):
    """Each watchdog can work independently
    it may help you find the right topic
    and monit a post that didn't appear

    it will send message to the post once it released
    """

    def __init__(self, user, config):
        self._session = requests.Session()
        self._user = user
        self._config = config

        print "{}:{} init the watchdog".format(self, self._user)

    def monit(self):
        try:
            auth = Auth(self._session, self._user, self._config)
            auth.confirm()
        except Exception:
            return None

        try:
            topic = Topic(self._session, self._user, self._config)
            post_url = topic.process()

            nt = Post(self._session, self._user, self._config, post_url)
            nt.reply()
        except Exception:
            return None

    def __repr__(self):
        return "<WatchDog>"


def dispatch(fpath):
    configs = configparser.ConfigParser()
    configs.read(fpath)

    dog_ls = []
    for user, config in configs.iteritems():
        if user == "DEFAULT":
            continue

        dog = WatchDog(user, config)
        dog_ls.append(gevent.spawn(dog.monit))

    gevent.joinall(dog_ls)

    print "all is finished"


# XXX add log level
def main():
    dispatch("./instance/config.ini")


if "__main__" == __name__:
    main()
