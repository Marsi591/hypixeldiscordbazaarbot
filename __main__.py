import discord
from discord.ext import commands, tasks
import math
import requests
import json
import time
import config
import hypixel_api
import random

hypixel = hypixel_api.HypixelApi()
responses = config.RESPONSES
print(responses)
intents = discord.Intents.default()
intents.message_content = True
prefix = config.GLOBAL_CONFIG["prefix"]
bot = commands.Bot(command_prefix=prefix, intents=intents)

bazaar_data = None

def f_num(number, decimals=0):
    return f"{round(number, decimals):,}"

@bot.event
async def on_ready():
    await bot.add_cog(BazaarCog(bot))


class BazaarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {
            "margin": 250,
            "volume": 1000000,
        }
        self.embed_list = ()

    @commands.command()
    async def bz(self, ctx, arg):
        item = hypixel.items.get_item_by_id(arg)
        embed = discord.Embed(
            title=f"You wanted to know about {item.name} ~?",
            color=0xffffff
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=time.ctime(time.time()))
        embed.add_field(
            name=item.name,
            value=f"BUY: {round(item.bz_price['buy'],2):,} coins\nSELL: {round(item.bz_price['sell'],2):,} coins\n7d SALES: {item.bz_moving_week['sell']:,}"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def margin(self, ctx, ammount, t_type):
        if t_type == "percent":
            ctx.send(f"Set margin tracker to {ammount}% of the total price.")
        if t_type == "coins":
            ctx.send(f"Set margin tracker to {ammount}% coins.")

    @commands.command()
    async def spike(self, ctx, ammount, t_type):
        if t_type == "percent":
            ctx.send(f"Set spike tracker to {ammount}% of the total price.")
        if t_type == "coins":
            ctx.send(f"Set spike tracker to {ammount}% coins.")

    @commands.command()
    async def sell_volume(self, ctx, ammount):
        ctx.send(f"Set the tacker sell volume to {ammount} sellers.")

    @commands.command()
    async def buy_volume(self, ctx, ammount):
        ctx.send(f"Set the tacker buy volume to {ammount} sellers.")

    @commands.command()
    async def brief(self, ctx):
        new_search = hypixel.bazaar.limit_search()
        new_search.add_limit("margin", False, self.settings["margin"])
        new_search.add_limit("sellVolume", False, self.settings["volume"])
        results = new_search.finalize()
        embed = discord.Embed(
            title=random.choice(responses),
            color=0xb05b48,
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=time.ctime(time.time()))

        for i in results:

            embed.add_field(
                name=f"{i.name}",
                value=f"MARGIN: {math.floor(i.bz_price['margin']):,}\nBUY: {math.floor(i.bz_price['buy']):,}\nSELL: {math.floor(i.bz_price['sell']):,}",
                inline=False
            )
            # await ctx.send(f"{i.name} has a margin of {i.bz_price['margin']:,} coins")
            # await ctx.send(f"BUY: {i.bz_price['buy']} SELL: {i.bz_price['sell']}")
        await ctx.send(embed=embed)

    @commands.command()
    async def notify_me(self, ctx, item, above_below, price_per_item):
        pass


bot.run(config.GLOBAL_CONFIG["discord_token"])
