# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import redis
import os
from mzitu.items import MzituItem

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

HASH_KEY_PHOTO = "mzitu_hash_photo"
LIST_KEY_IMAGE = "list_image"


class DownloadSpider(RedisSpider):
    name = 'download'
    allowed_domains = ['mzitu.com']
    redis_key = LIST_KEY_IMAGE

    def parse(self, response):
        json = REDIS.hget(HASH_KEY_PHOTO, response.url).decode()
        album = MzituItem(eval(json))
        dirs = os.path.split(album['file_path'])[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        open(album['file_path'], 'wb').write(response.body)
