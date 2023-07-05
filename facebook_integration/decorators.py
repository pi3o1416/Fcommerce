
from concurrent import futures
import time
import functools


def retry_on_connection_error(number_of_retry):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(number_of_retry + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except ConnectionError:
                    time.sleep(2**i)
            raise ConnectionError(f"Failed to connect after {number_of_retry} retry")
        return wrapper
    return decorator


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with futures.ThreadPoolExecutor() as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timeout=seconds)
                except futures.TimeoutError:
                    raise TimeoutError("Function took too long to response")
            return result
        return wrapper
    return decorator
