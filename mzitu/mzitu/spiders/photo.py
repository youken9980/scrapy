# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
import redis
import os
from mzitu.items import MzituItem

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

LIST_KEY_ALBUM = "mzitu_list_album"
HASH_KEY_PHOTO = "mzitu_hash_photo"
LIST_KEY_IMAGE = "list_image"
IMAGE_HOME = "/Volumes/Destiny/Image/scrapy/mzitu"


class PhotoSpider(RedisSpider):
    name = 'photo'
    allowed_domains = ['mzitu.com']
    redis_key = LIST_KEY_ALBUM

    def parse(self, response):
        for item in response.css('div.main-image img'):
            photo = MzituItem()
            photo['url'] = item.css('img::attr("src")').extract_first()
            photo_desc = item.css('img::attr("alt")').extract_first()
            year = photo['url'].split("/")[3]
            file_name = os.path.split(photo['url'])[1]
            photo['file_path'] = "%s/%s/%s/%s" % (IMAGE_HOME, year, photo_desc, file_name)
            if not REDIS.hexists(HASH_KEY_PHOTO, photo['url']):
                REDIS.hset(HASH_KEY_PHOTO, photo['url'], photo)
                REDIS.lpush(LIST_KEY_IMAGE, photo['url'])
        next_page = None
        for item in response.css("div.pagenavi a"):
            if "下一页" in item.css('a span::text').extract_first():
                next_page = item.css('a::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)
