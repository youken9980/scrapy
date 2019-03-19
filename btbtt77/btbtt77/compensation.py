#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis
import os
from items import Btbtt77Item

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6379
REDIS_CONN_POOL = redis.ConnectionPool(host=SERVER_IP, port=SERVER_PORT)
REDIS = redis.Redis(connection_pool=REDIS_CONN_POOL)

DOMAIN = "btbtt77.com"
PHOTO_HASH = "%s_photo_hash" % DOMAIN
PHOTO_LIST = "%s_photo_list" % DOMAIN

print("正在运行补偿任务，加载Redis数据中，请稍候……")
for key in REDIS.hkeys(PHOTO_HASH):
    json = REDIS.hget(PHOTO_HASH, key).decode()
    photo = Btbtt77Item(eval(json))
    if not (os.path.exists(photo['file_path']) and os.access(photo['file_path'], os.R_OK)):
        REDIS.lpush(PHOTO_LIST, key.decode())
print("运行完毕，共加载%s项" % (REDIS.llen(PHOTO_LIST)))
