# -*- coding: utf-8 -*-

import sys

import scrapy

from .const import *
from ..items import Btbtt77Item

sys.path.append("../../")
from utils.redis import REDIS


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
