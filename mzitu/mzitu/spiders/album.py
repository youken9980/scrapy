# -*- coding: utf-8 -*-
import redis
import scrapy

from ..items import MzituItem

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

HASH_KEY_ALBUM = "mzitu_hash_album"
LIST_KEY_ALBUM = "mzitu_list_album"


class AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/all/', 'http://www.mzitu.com/old/']

    def parse(self, response):
        for item in response.css('div.all a'):
            album = MzituItem()
            album['url'] = item.css('a::attr("href")').extract_first()
            album['desc'] = item.css('a::text').extract_first()
            if not REDIS.hexists(HASH_KEY_ALBUM, album['url']):
                REDIS.hset(HASH_KEY_ALBUM, album['url'], album)
                REDIS.lpush(LIST_KEY_ALBUM, album['url'])
