from fastapi import Request
from fastapi.params import Depends  # The real Depends class
from utils import ConnectionUtil


class CallableDepends(Depends):
    """Depends with __call__ implemented as a shortcut to Depends.dependency()."""

    def __call__(self, *args, **kwargs):
        return self.dependency(*args, **kwargs)


def dependency(func=None, *, use_cache: bool = True):
    def decorator(wrap):
        return CallableDepends(dependency=wrap, use_cache=use_cache)

    # Allow decorator to be used without calling it
    if callable(func):
        return decorator(func)

    return decorator


@dependency()
async def get_app(request: Request):
    """Dependency to get the serving app."""
    return request.state.app


@dependency()
async def get_bot(request: Request):
    """Dependency to get the running bot."""
    # In case how we get the app is changed
    return (await get_app(request)).bot


@dependency()
async def get_conn(request: Request) -> ConnectionUtil:
    """Dependency to get a ConnectionUtil connection to work with."""
    return ConnectionUtil((await get_bot(request)).pool)
