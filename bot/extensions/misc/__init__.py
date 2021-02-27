from extensions.misc import eight_ball, send


async def init(bot):
    """Initialize the necessary database features."""
    async with bot.pool.acquire() as conn:
        # 8ball
        await conn.execute("""CREATE SEQUENCE eightball_sqc;""")
        await conn.execute("""
            CREATE TABLE eightball (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('eightball_sqc'),
                response TEXT NOT NULL,
                weight SMALLINT NOT NULL DEFAULT 1
            );
        """)
        await conn.execute("""ALTER SEQUENCE eightball_sqc OWNED BY eightball.id;""")

        await conn.execute("""CREATE INDEX eightball_weight_idx ON eightball (id, weight);""")


def setup(bot):
    if bot.init:
        return bot.loop.run_until_complete(init(bot))

    bot.add_command(eight_ball.eightball)
    bot.app.include_router(eight_ball.api)

    bot.add_command(send.send)
