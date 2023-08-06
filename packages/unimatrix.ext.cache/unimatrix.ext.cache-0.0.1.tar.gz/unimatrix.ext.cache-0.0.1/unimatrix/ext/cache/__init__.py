# pylint: skip-file
from .manager import connections


__all__ = []


async def get(key, using='default', *args, **kwargs):
    """Return given `key` from the cache `using`."""
    return await connections[using].get(key, *args, **kwargs)


async def set(key, value, using='default', *args, **kwargs):
    """Set the given `key` to `value`."""
    return await connections[using].set(key, value, *args, **kwargs)
