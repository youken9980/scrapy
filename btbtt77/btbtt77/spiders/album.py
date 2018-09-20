# -*- coding: utf-8 -*-
import scrapy
import redis
from btbtt77.items import Btbtt77Item

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

HASH_KEY_ALBUM = "btbtt77_hash_album"
LIST_KEY_ALBUM = "btbtt77_list_album"


class Btbtt77AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = ['btbtt77.com']
    start_urls = ['http://www.btbtt77.com/forum-index-fid-8.htm']

    def parse(self, response):
        for item in response.css('div.body a.thread-new'):
            album = Btbtt77Item()
            album['url'] = item.css('a::attr("href")').extract_first()
            album['desc'] = item.css('a::text').extract_first()
            if not REDIS.hexists(HASH_KEY_ALBUM, album['url']):
                REDIS.hset(HASH_KEY_ALBUM, album['url'], album)
                REDIS.lpush(LIST_KEY_ALBUM, album['url'])
        for item in response.css('div.body a.thread-old'):
            album = Btbtt77Item()
            album['url'] = item.css('a::attr("href")').extract_first()
            album['desc'] = item.css('a::text').extract_first()
            if not REDIS.hexists(HASH_KEY_ALBUM, album['url']):
                REDIS.hset(HASH_KEY_ALBUM, album['url'], album)
                REDIS.lpush(LIST_KEY_ALBUM, album['url'])
        next_page = response.css('div.page a.checked + a::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)
