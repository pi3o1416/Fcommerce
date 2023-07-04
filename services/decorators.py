import signal
import functools


def handle_timeout(signum, frame):
    raise TimeoutError("Function took too long to response")


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # cancel the alarm signal
            return result
        return wrapper
    return decorator
