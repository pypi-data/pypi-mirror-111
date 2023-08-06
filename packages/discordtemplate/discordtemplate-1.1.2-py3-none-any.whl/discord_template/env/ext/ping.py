import discord
from discord.ext import commands
import time


class Ping(commands.Cog):
    """
    A main `:class:` for Ping.
        Usage:
            <prefix>ping
        Response:
            Ping: 30ms!

    """
    def __init__(self,bot):
        self.bot = bot
        

    @commands.command(pass_context=True)
    async def ping(self,ctx):
        async with ctx.typing():
            t1 = time.perf_counter()
        
        t2 = time.perf_counter()
        await ctx.send("Ping: {}ms".format(round((t2-t1)*1000)))


def setup(bot):
    bot.add_cog(Ping(bot))
