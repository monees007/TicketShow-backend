from flask_caching import Cache

from application.config import cacheConfig

cache = Cache(config=cacheConfig)
