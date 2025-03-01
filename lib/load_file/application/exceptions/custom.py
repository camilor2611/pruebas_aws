import functools

from pydantic import ValidationError


def exception_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"success": False, "data": str(e)}
        except Exception as e:
            return {"success": False, "data": str(e)}
    return wrapper
