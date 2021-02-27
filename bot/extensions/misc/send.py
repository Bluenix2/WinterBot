import discord
from discord.ext import commands


@commands.command(hidden=True)
async def send(ctx, *, text):
    await ctx.message.delete()

    # Figure out if the first "argument" is a channel and use that instead:
    words = text.split(' ')
    try:
        channel = await commands.TextChannelConverter().convert(ctx, words[0])
    except commands.BadArgument:
        channel = ctx.channel
    else:
        words = words[1:]  # Skip the channel we just detected

    await channel.send(
        ' '.join(words),  # Recreate the text
        allowed_mentions=discord.AllowedMentions.none()
    )
