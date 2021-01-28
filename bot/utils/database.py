from typing import Any, Optional, Union

import asyncpg
from discord.ext import commands


class ContextPoolAcquire:
    """Utilization class for pool connection, mimics asyncpg.
    Its implementation allows all of the following usages:

    ```python

    # One-time use
    await ctx.fetch(...)

    # Contextual behaviour
    async with ctx.acquire() as conn:
        ...

    # Get the connection
    conn = await ctx.acquire()

    # Reuse same connection
    await ctx.acquire()
    await ctx.fetch(...)
    await ctx.execute(...)

    ```
    """

    __slots__ = ('ctx', 'timeout')

    def __init__(self, connection, timeout: float) -> None:
        self.ctx: ConnectionUtil = connection
        self.timeout: float = timeout

    def __await__(self):
        # We can't await inside a synchronous function,
        # so instead we directly call the corountine's __await__.
        return self.connection._acquire(self.timeout).__await__()

    async def __aenter__(self):
        return await self.connection._acquire(self.timeout)

    async def __aexit__(self, *_):
        await self.connection.release()


class ConnectionUtil:
    """Util for working with a database connection."""
    def __init__(self, pool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pool: asyncpg.pool.Pool = pool or self.bot.pool  # Context subclass
        self._conn: Optional[asyncpg.Connection] = None

    @property
    def conn(self) -> Union[asyncpg.Connection, asyncpg.pool.Pool]:
        return self._conn or self.pool

    # Shortcuts

    async def execute(self, *args, **kwargs) -> Any:
        return await self.conn.execute(*args, **kwargs)

    async def executemany(self, *args, **kwargs) -> Any:
        return await self.conn.executemany(*args, **kwargs)

    async def fetch(self, *args, **kwargs) -> Any:
        return await self.conn.fetch(*args, **kwargs)

    async def fetchval(self, *args, **kwargs) -> Any:
        return await self.conn.fetchval(*args, **kwargs)

    async def fetchrow(self, *args, **kwargs) -> Any:
        return await self.conn.fetchrow(*args, **kwargs)

    # Cached pool connection

    async def _acquire(self, timeout: float) -> asyncpg.Connection:
        if self._conn is None:
            self._conn = await self.pool.acquire(timeout=timeout)
        return self._conn

    def acquire(self, timeout: float = 30.0) -> ContextPoolAcquire:
        """Acquire a database connection from the pool,
        this can be awaited, see `ContextPoolAcquire.
        """
        return ContextPoolAcquire(self, timeout)

    async def release(self) -> None:
        """Release the database connection back to the pool,
        this is completely safe even if you never called `acquire()`.
        """
        if self._conn is None:
            return

        await self.pool.release(self._conn)
        self._conn = None


class Context(ConnectionUtil, commands.Context):
    """Custom context class with some extra methods for convenience."""
    pass
