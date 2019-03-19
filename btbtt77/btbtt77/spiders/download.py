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
PHOTO_HASH = "%s_photo_hash" % DOMAIN
PHOTO_LIST = "%s_photo_list" % DOMAIN


class DownloadSpider(RedisSpider):
    name = 'download'
    allowed_domains = [DOMAIN]
    redis_key = PHOTO_LIST

    def parse(self, response):
        json = REDIS.hget(PHOTO_HASH, response.url).decode()
        album = Btbtt77Item(eval(json))
        dirs = os.path.split(album['file_path'])[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        open(album['file_path'], 'wb').write(response.body)
