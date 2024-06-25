# from typing import Optional, Union
#
# from redis.lock import Lock
#
# from server import settings
#
#
# def flushall():
#     if not settings.CACHING_ENABLED:
#         return
#     from django.core.cache import cache
#     cache.clear()
#
#
# def lock(key: str, blocking: bool = False, blocking_timeout: Union[int, float, None] = None, ttl: Union[int, float, None] = 300) -> Optional[Lock]:
#     if not settings.CACHING_ENABLED:
#         return None
#     from django_redis import get_redis_connection
#     client = get_redis_connection("default")
#     return client.lock(key, blocking=blocking, blocking_timeout=blocking_timeout, timeout=ttl)
#
#
# def delete(key: str):
#     if not settings.CACHING_ENABLED:
#         return None
#     from django.core.cache import cache
#     cache.delete(key)
#
#
