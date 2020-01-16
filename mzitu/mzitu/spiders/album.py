# -*- coding: utf-8 -*-

import sys

import scrapy

from .const import *
from ..items import MzituItem

sys.path.append("../../")
from utils.redis import REDIS


class AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/all/', 'http://www.mzitu.com/old/']

    def parse(self, response):
        for item in response.css('div.all a'):
            album = MzituItem()
            album['url'] = item.css('a::attr("href")').extract_first()
            album['desc'] = item.css('a::text').extract_first()
            if not REDIS.hexists(ALBUM_HASH, album['url']):
                REDIS.hset(ALBUM_HASH, album['url'], album)
                REDIS.lpush(ALBUM_LIST, album['url'])
