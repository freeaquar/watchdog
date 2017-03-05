#!/usr/bin/env python
# -*- coding: utf8 -*-

import arrow


def url_trim(url):
    return url.replace("&amp;", "&")


class RecorderLevel(object):
    info = 1
    warn = 2
    error = 3


class Recorder(object):
    """format info and print out"""
    current_level = RecorderLevel.info
    level_msg = {
        RecorderLevel.info: "INFO",
        RecorderLevel.warn: "WARN",
        RecorderLevel.error: "ERROR",
    }

    @classmethod
    def info(cls, obj, user, msg, e):
        cls._print(RecorderLevel.info, obj, user, msg, e="")

    @classmethod
    def warn(cls, obj, user, msg, e):
        cls._print(RecorderLevel.warn, obj, user, msg, e="")

    @classmethod
    def error(cls, obj, user, msg, e):
        cls._print(RecorderLevel.warn, obj, user, msg, e="")

    @classmethod
    def _output(cls, level, obj, user, msg, e):
        if level < cls.current_level:
            return None

        data = arrow.now().format('YYYY-MM-DD HH:mm:ss')
        e = e or " [{}|{}]".format(type(e) + str(e))

        print "[{level_msg}] {date}: {obj}-{user} {msg} {e}".format(
            level_msg=cls.level_msg[level], data=data, obj=obj, user=user,
            msg=msg, e=e
        )
