#!/usr/bin/env python3
"""Cache"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable) -> None:
    """ display the history of calls of a particular function."""

    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    call_count = len(inputs)

    print(f"{method_name} was called {call_count} times:")

    for input_value, output_value in zip(inputs, outputs):
        input_str = input_value.decode('utf-8')
        output_str = output_value.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache():
    """class cache"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a randomly generated key"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes, int, float, None]:
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
