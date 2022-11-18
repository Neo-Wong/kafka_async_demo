# coding=utf-8
"""
author = neowong
"""

import hashlib
import uuid


def get_md5(content):
    c_md5 = hashlib.md5()
    c_md5.update(content.encode("utf-8"))
    return c_md5.hexdigest()


def get_rand_16():
    return get_md5_16(uuid.uuid1().hex)


def get_md5_16(content):
    return get_md5(content)[8:-8]