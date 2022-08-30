import functools
from datetime import datetime


def benchmark(func):
    @functools.wraps(func)
    def _benchmark(*args, **kwargs):
        start = datetime.now()
        print(f"{func.__name__:>20} start: {start}")
        result = func(*args, **kwargs)
        end = datetime.now()
        print(f"{func.__name__:>20}   end: {end}")
        delta = end - start
        total = delta.total_seconds()
        print(f"{func.__name__:>20} total: {total}")
        return result

    return _benchmark
