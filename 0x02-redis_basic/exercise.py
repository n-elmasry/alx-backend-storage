#!/usr/bin/env python3
"""Cache"""
import redis
import uuid
from typing import Union,  Callable, Optional


class Cache():
    """class cache"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a randomly generated key"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis by key and optionally apply a function"""
        value = self._redis.get(key)

        if value is None:
            return None

        if fn is not None:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """returns str(get)"""
        return self._redis.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """returns int(get)"""
        return self.get(key, fn=int)
