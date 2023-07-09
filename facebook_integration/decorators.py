
import logging
from concurrent import futures
import time
import functools
from .exceptions import FacebookAPIErrorException


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


def log_api_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('fcommerce')
        # Retrieve Merchant from FacebookAdapter Instance args[0] refer to self
        merchant = args[0].merchant
        try:
            result = func(*args, **kwargs)
            return result
        except FacebookAPIErrorException as exception:
            logger.error({
                "function": func.__name__,
                "message": exception.message,
                "response": exception.response.json() if exception.response is not None else None,
                "status_code": exception.response.status_code if exception.response is not None else None,
                "merchant_id": merchant.merchant_id
            })
    return wrapper
