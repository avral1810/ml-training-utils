from functools import wraps
from time import perf_counter
from typing import Any, Callable, Iterator
from contextlib import contextmanager

@contextmanager
def _timer(name: str) -> Iterator[None]:
    start = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(f"{name} completed in {elapsed:.2f}s")


def time_execution(arg: str | Callable[..., Any]) -> Any:
    if callable(arg):
        func = arg
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with _timer(func.__name__):
                return func(*args, **kwargs)
        return wrapper
    return _timer(arg)
