# scrapy

1. docker run redis
```shell
docker run -d -p 6379:6379 \
  -v ~/dockerVolumn/redis/data:/data \
  --network mynet --name redis-local \
  redis redis-server --appendonly yes
```

2. scrapy crawl
```shell
cd foo/bar
scrapy crawl album
scrapy crawl photo
scrapy crawl download
```

