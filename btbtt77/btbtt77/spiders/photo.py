# -*- coding: utf-8 -*-
import os
import sys

from scrapy_redis.spiders import RedisSpider

from .const import *
from ..items import Btbtt77Item

sys.path.append("../../")
from utils.redis import REDIS


class Btbtt77PhotoSpider(RedisSpider):
    name = 'photo'
    allowed_domains = [DOMAIN]
    redis_key = ALBUM_LIST

    def parse(self, response):
        index = 0
        photo_desc = response.css('meta[name=keywords]::attr("content")').extract_first()
        for photo_url in response.css('div.message img::attr("src")').extract():
            photo = Btbtt77Item()
            photo['url'] = photo_url
            index += 1
            suffix = os.path.splitext(photo_url)[1]
            photo['file_path'] = "%s/%s/%s%s" % (IMAGE_HOME, photo_desc, index, suffix)
            if not REDIS.hexists(PHOTO_HASH, photo['url']):
                REDIS.hset(PHOTO_HASH, photo['url'], photo)
                REDIS.lpush(PHOTO_LIST, photo['url'])
