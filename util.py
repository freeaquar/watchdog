#!/usr/bin/env python
# -*- coding: utf8 -*-

import arrow


def url_trim(url):
    return url.replace("&amp;", "&")


class RecorderLevel(object):
    debug = 1
    info = 2
    warn = 3
    error = 4


class Recorder(object):
    """format info and print out"""

    current_level = RecorderLevel.info
    _level_msg = {
        RecorderLevel.debug: "DEBUG",
        RecorderLevel.info: "INFO",
        RecorderLevel.warn: "WARN",
        RecorderLevel.error: "ERROR",
    }

    @classmethod
    def debug(cls, obj, user, msg, e=""):
        cls._output(RecorderLevel.debug, obj, user, msg, e)

    @classmethod
    def info(cls, obj, user, msg, e=""):
        cls._output(RecorderLevel.info, obj, user, msg, e)

    @classmethod
    def warn(cls, obj, user, msg, e=""):
        cls._output(RecorderLevel.warn, obj, user, msg, e)

    @classmethod
    def error(cls, obj, user, msg, e=""):
        cls._output(RecorderLevel.error, obj, user, msg, e)

    @classmethod
    def _output(cls, level, obj, user, msg, e):
        if level < cls.current_level:
            return None

        date = arrow.now().format('YYYY-MM-DD HH:mm:ss')
        e = e and " [{}|{}]".format(type(e), str(e))

        print "[{level_msg}] {date}: {obj}-{user} {msg} {e}".format(
            level_msg=cls._level_msg[level], date=date, obj=obj, user=user,
            msg=msg, e=e
        )
