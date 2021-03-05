from bot.extensions.misc import eight_ball, send


def setup(bot):
    # 8ball
    bot.add_command(eight_ball.eightball)
    bot.app.include_router(eight_ball.api)

    # Send
    bot.add_command(send.send)
