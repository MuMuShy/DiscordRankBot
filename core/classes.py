import discord
from discord.ext import commands
from discord.ext import tasks

class Cog_Extension(commands.cog):
    def __init__(self,bot):
        self.bot = bot