# imports
import discord
from discord.ext import commands, tasks
import os
import config
import asyncio

# Create bot variable
intents = discord.Intents.default()
intents.message_content = True
prefix = config.GLOBAL_CONFIG["prefix"]
bot = commands.Bot(command_prefix=prefix, intents=intents)

# setup cogs upon bot loading
@bot.event
async def setup_hook():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f'Cogs.{filename[:-3]}')

# Add reset command
@bot.event
async def on_ready():
    await bot.add_cog(Reload(bot))
    print('loaded')

# Reload cogs command
class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx):
        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py"):
                await bot.unload_extension(f'Cogs.{filename[:-3]}')
                await bot.load_extension(f'Cogs.{filename[:-3]}')
        await ctx.send("https://tenor.com/view/aleks-workshop-reloading-reload-gif-20710655")


# Run bot
bot.run(config.GLOBAL_CONFIG["discord_token"])
