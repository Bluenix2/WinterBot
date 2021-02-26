import asyncio
import datetime
import sys
import traceback
from typing import Tuple

import asyncpg
import config
import utils
from discord.ext import commands
from fastapi import FastAPI
from uvicorn import Config, Server

initial_extensions: Tuple[str] = (
    'extensions.misc',
)


class WinterBot(commands.Bot):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(command_prefix='?')

        self.app: FastAPI = app

        self.client_id: int = config.client_id

        try:
            self.pool: asyncpg.pool.Pool = self.loop.run_until_complete(
                asyncpg.create_pool(config.postgresql)
            )
        except asyncpg.PostgresError as e:
            print('Failed to setup PostgreSQL connection', file=sys.stderr)
            raise e

        try:
            self.init = (sys.argv[1] == 'init')
        except IndexError:
            self.init = False

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except commands.ExtensionError:
                print(f'Failed to load extension {extension}', file=sys.stderr)
                traceback.print_exc()

        if self.init:
            print('Initialized database tables')
            exit(0)

    async def on_ready(self) -> None:
        # on_ready can be called multiple times,
        # we don't want to override previous values.
        if not hasattr(self, 'uptime'):
            self.uptime: datetime.datetime = datetime.datetime.utcnow()

        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def process_commands(self, message) -> None:
        ctx = await self.get_context(message, cls=utils.Context)

        try:
            await self.invoke(ctx)
        finally:
            # No matter what happens, if we have any outstanding connections
            await ctx.release()

    async def serve(self, **kwargs) -> None:
        """Start serving the web app with Uvicorn. This will not resume control
        until the server terminates.
        """
        server = Server(config=Config(self.app, **kwargs))

        return await server.serve()

    async def start(self, token, *, bot=True, reconnect=True, **kwargs):
        """Shorthand coroutine for starting the bot and app, control is not resumed until
        the Discord WebSocket is terminated or Uvicorn server killed.
        """
        await self.login(token, bot=bot)
        tasks = (
            asyncio.create_task(self.serve(**kwargs)),
            asyncio.create_task(self.connect(reconnect=reconnect))
        )
        # If any one of them complete that means they died
        return await asyncio.wait(tasks, loop=self.loop, return_when=asyncio.FIRST_COMPLETED)

    def run(self) -> None:
        return super().run(config.token)


# Make sure this is not ran if the file is imported
if __name__ == '__main__':
    app = FastAPI()

    bot = WinterBot(app)

    app.bot = bot

    bot.run()
