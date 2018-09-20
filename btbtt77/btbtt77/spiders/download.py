# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import redis
import os
from btbtt77.items import Btbtt77Item

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

HASH_KEY_PHOTO = "btbtt77_hash_photo"
LIST_KEY_IMAGE = "list_image:test"


class DownloadSpider(RedisSpider):
    name = 'download'
    redis_key = LIST_KEY_IMAGE

    def parse(self, response):
        json = REDIS.hget(HASH_KEY_PHOTO, response.url).decode()
        album = Btbtt77Item(eval(json))
        dirs = os.path.split(album['file_path'])[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        open(album['file_path'], 'wb').write(response.body)