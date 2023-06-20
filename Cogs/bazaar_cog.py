# Imports
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

# Variables
hypixel = hypixel_api.HypixelApi()
responses = config.RESPONSES
bazaar_data = None

# Miscellanious Functions


def f_num(number, decimals=0):
    return f"{round(number, decimals):,}"


def f_coins(number):
    return "$" + f_num(number, decimals=0)


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
            color=0xF5A9B8
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=time.ctime(hypixel.bazaar.creation_date))
        embed.add_field(
            name=item.name,
            value=f"BUY: {f_coins(item.bz_price['buy'])}\nSELL: {f_coins(item.bz_price['sell'])}\n7d SALES: {f_num(item.bz_moving_week['sell'])}"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def begin_tracking(self, ctx):
        pass

    @commands.command()
    async def brief(self, ctx):
        new_search = hypixel.bazaar.limit_search()
        new_search.add_limit("margin", False, self.settings["margin"])
        new_search.add_limit("sellVolume", False, self.settings["volume"])
        results = new_search.finalize()
        results.sort(key=lambda x: x.bz_price["margin"], reverse=True)
        embed = discord.Embed(
            title=random.choice(responses),
            color=0xF5A9B8,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=time.ctime(hypixel.bazaar.creation_date))
        embeds = []
        i=0
        while i < len(results):
            new_embed = copy.deepcopy(embed)
            e=0
            while e < 5 and i < len(results):
                item = results[i]
                new_embed.add_field(
                    name=f"{item.name}",
                    value=f"MARGIN: {f_coins(item.bz_price['margin'])}\nBUY: {f_coins(item.bz_price['buy'])}\nSELL: {f_coins(item.bz_price['sell'])}",
                    inline=False
                )
                i+=1
                e+=1
            embeds.append(new_embed)
        await Paginator.Simple().start(ctx, pages=embeds)

    @commands.command()
    async def notify_me(self, ctx, item, above_below, price_per_item):
        pass


async def setup(bot):
    await bot.add_cog(BazaarCog(bot))
