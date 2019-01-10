# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mian
   Description :    入口函数
   Author :       wsm
   date：          2019-01-10
-------------------------------------------------
   Change Activity:
                   2019-01-10:
-------------------------------------------------
"""
__author__ = 'wsm'

from scrapy.cmdline import execute

execute(["scrapy", "crawl", "jobbole"])