import discord
import asyncio
from discord.ext import commands
import discord
from discord.ext import commands, tasks
import time
import config
import hypixel_api
import random
import Paginator
import copy
class AHCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.item_list = config.ITEMS
        
    @commands.command()
    async def ahflip(self, ctx):
        for item in self.item_list:
            print('gaming')
            



async def setup(bot):
    await bot.add_cog(AHCog(bot))