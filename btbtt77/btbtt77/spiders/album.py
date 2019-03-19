# -*- coding: utf-8 -*-
import scrapy
import redis
from btbtt77.items import Btbtt77Item

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

DOMAIN = "btbtt77.com"
ALBUM_HASH = "%s_album_hash" % DOMAIN
ALBUM_LIST = "%s_album_list" % DOMAIN
START_URL = "http://%s/forum-index-fid-8.htm" % DOMAIN


class Btbtt77AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = [DOMAIN]
    start_urls = [START_URL]

    def parse(self, response):
        for item in (response.css('div.body a.thread-old') + response.css('div.body a.thread-new')):
            album = Btbtt77Item()
            album['url'] = item.css('a::attr("href")').extract_first()
            album['desc'] = item.css('a::text').extract_first()
            if not REDIS.hexists(ALBUM_HASH, album['url']):
                REDIS.hset(ALBUM_HASH, album['url'], album)
                REDIS.lpush(ALBUM_LIST, album['url'])
        next_page = response.css('div.page a.checked + a::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)
