# -*- coding: utf-8 -*-
import os
import sys

from scrapy_redis.spiders import RedisSpider

from .const import *
from ..items import MzituItem

sys.path.append("../../")
from utils.redis import REDIS


class DownloadSpider(RedisSpider):
    name = 'download'
    allowed_domains = ['mzitu.com']
    redis_key = PHOTO_LIST

    def parse(self, response):
        json = REDIS.hget(PHOTO_HASH, response.url).decode()
        album = MzituItem(eval(json))
        dirs = os.path.split(album['file_path'])[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        open(album['file_path'], 'wb').write(response.body)
