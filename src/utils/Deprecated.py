import warnings
import functools

def deprecated(func):
    warned = False
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal warned
        if not warned:
            warnings.warn(
                f"{func.__name__} is deprecated and will be removed in future versions",
                category=DeprecationWarning,
                stacklevel=2
            )
            warned = True
        return func(*args, **kwargs)
    return wrapper
