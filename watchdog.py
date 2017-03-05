#!/usr/bin/env python
# -*- coding: utf8 -*-

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import click
import requests
import configparser

from auth import Auth
from topic import Topic
from post import Post
from util import Recorder, RecorderLevel


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

        Recorder.info(self, self._user, "init")

    def monit(self):
        try:
            auth = Auth(self._session, self._user, self._config)
            auth.confirm()

            topic = Topic(self._session, self._user, self._config)
            nt = Post(self._session, self._user, self._config,
                      topic.locate_post_url())

            nt.reply()
        except Exception as e:
            Recorder.error(self, self._user, "init the watchdog", e)
            return None

    def __repr__(self):
        return "<WatchDog>"


def dispatch(fpath):
    Recorder.info("<dispatch>", "main", "ready to dispatch")

    configs = configparser.ConfigParser()
    configs.read(fpath)

    dog_ls = []
    for user, config in configs.iteritems():
        if user == "DEFAULT":
            continue

        dog = WatchDog(user, config)
        dog_ls.append(gevent.spawn(dog.monit))

    gevent.joinall(dog_ls)

    Recorder.info("<dispatch>", "main", "all is finished")


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--log-level", required=False,
              type=click.Choice(["debug", "info", "warning", "error"]),
              default="info", show_default=True, help="Log level")
def main(log_level):
    Recorder.current_level = getattr(RecorderLevel, log_level)
    dispatch("./instance/config.ini")


if "__main__" == __name__:
    main()
