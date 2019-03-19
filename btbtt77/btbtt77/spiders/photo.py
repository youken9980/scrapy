# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import redis
import os
from btbtt77.items import Btbtt77Item

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

DOMAIN = "btbtt77.com"
ALBUM_LIST = "%s_album_list" % DOMAIN
PHOTO_HASH = "%s_photo_hash" % DOMAIN
PHOTO_LIST = "%s_photo_list" % DOMAIN
IMAGE_HOME = "~/Downloads/scrapy/%s" % DOMAIN


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
