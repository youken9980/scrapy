# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import redis
import os
from btbtt77.items import Btbtt77Item

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

LIST_KEY_ALBUM = "btbtt77_list_album"
HASH_KEY_PHOTO = "btbtt77_hash_photo"
LIST_KEY_IMAGE = "list_image"
IMAGE_HOME = "/Volumes/Destiny/Image/scrapy/btbtt77"


class Btbtt77PhotoSpider(RedisSpider):
    name = 'photo'
    allowed_domains = ['btbtt77.com']
    redis_key = LIST_KEY_ALBUM

    def parse(self, response):
        index = 0
        photo_desc = response.css('meta[name=keywords]::attr("content")').extract_first()
        for photo_url in response.css('div.message img::attr("src")').extract():
            index += 1
            suffix = os.path.splitext(photo_url)[1]
            album = Btbtt77Item()
            album['url'] = photo_url
            album['file_path'] = "%s/%s/%s%s" % (IMAGE_HOME, photo_desc, index, suffix)
            if not REDIS.hexists(HASH_KEY_PHOTO, album['url']):
                REDIS.hset(HASH_KEY_PHOTO, album['url'], album)
                REDIS.lpush(LIST_KEY_IMAGE, album['url'])
