#!/usr/bin/env python3
"""
A basic Redis utility.
"""

from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for
    a specific function.
    """
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that increments the count for a specific key every
    time the method is called.
    Returns the value returned by the original method.
    """
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls for a particular function.
    """
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache:
    """
    Cache class to handle Redis operations.
    """
    def __init__(self):
        """
        Initializes an instance of the Redis client.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Takes and stores a data argument and returns a string key.
        """
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """
        Retrieves data associated with a key.
        Optionally converts the data using the provided callable (fn).
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: str) -> str:
        """
        Returns the string value of decoded bytes.
        """
        return data.decode('utf-8', 'strict')

    def get_int(self, data: str) -> int:
        """
        Returns the integer value of decoded bytes.
        """
        return int(data)
