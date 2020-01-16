# -*- coding: utf-8 -*-
import os
import sys

import scrapy
from scrapy_redis.spiders import RedisSpider

from .const import *
from ..items import MzituItem

sys.path.append("../../")
from utils.redis import REDIS


class PhotoSpider(RedisSpider):
    name = 'photo'
    allowed_domains = ['mzitu.com']
    redis_key = ALBUM_LIST

    def parse(self, response):
        for item in response.css('div.main-image img'):
            photo = MzituItem()
            photo['url'] = item.css('img::attr("src")').extract_first()
            photo_desc = item.css('img::attr("alt")').extract_first()
            year = photo['url'].split("/")[3]
            file_name = os.path.split(photo['url'])[1]
            photo['file_path'] = "%s/%s/%s/%s" % (IMAGE_HOME, year, photo_desc, file_name)
            if not REDIS.hexists(PHOTO_HASH, photo['url']):
                REDIS.hset(PHOTO_HASH, photo['url'], photo)
                REDIS.lpush(PHOTO_LIST, photo['url'])
        next_page = None
        for item in response.css("div.pagenavi a"):
            if "下一页" in item.css('a span::text').extract_first():
                next_page = item.css('a::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)
