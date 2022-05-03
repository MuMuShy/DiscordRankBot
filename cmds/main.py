import discord
from discord.ext import commands
from discord.ext import tasks
from core.classes import Cog_Extension
class Main(Cog_Extension):
    @commands.command()
    async def rank(ctx):
        await ctx.send("123")

def setup(bot):
    bot.add_cog(Main(bot))

if __name__ == "__main__":
    pass