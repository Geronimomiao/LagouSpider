# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     common
   Description :
   Author :       wsm
   date：          2019-01-10
-------------------------------------------------
   Change Activity:
                   2019-01-10:
-------------------------------------------------
"""
__author__ = 'wsm'

import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()



