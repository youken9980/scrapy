# scrapy

#### install python, scrapy
```shell script
brew install python3
pip3 install redis==2.10.6
pip3 install scrapy
pip3 install scrapy-redis
pip3 freeze
```

#### docker run redis
```shell script
docker run -d -p 6379:6379 \
  -v ~/dockerVolumn/redis/data:/data \
  --network mynet --name redis-local \
  redis redis-server --appendonly yes
```

#### scrapy crawl
```shell script
scrapy shell <url>
```
or
```shell script
cd foo/bar
scrapy crawl album
scrapy crawl photo
scrapy crawl download
```
