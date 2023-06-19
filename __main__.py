import discord
from discord.ext import commands, tasks
import math
import requests
import json
import config
import hypixel_api

hypixel = hypixel_api.HypixelApi()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

bazaar_data = None


@bot.event
async def on_ready():
    await bot.add_cog(BazaarCog(bot))


class BazaarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {
            "margin": 500,
            "volume": 1000000,
        }

    @commands.command()
    async def bz(self, ctx, arg):
        item = hypixel.items.get_item_by_id(arg)
        await ctx.send(f"""{item.name}
        Buy Price: {item.bz_price["buy"]:,} coins
        Sell Price: {item.bz_price["sell"]:,} coins
        Sales in the past 7d: {item.bz_moving_week["sell"]:,} 
        """)

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
        await ctx.send(f"Here are the current items to look at based on the tracker settings:")
        new_search = hypixel.bazaar.limit_search()
        new_search.add_limit("volume", False, self.settings["volume"])
        results = new_search.finalize()
        for i in results:
            await ctx.send(f"{i.name} has a margin of {i.bz_price['margin']:,} coins")
            await ctx.send(f"BUY: {i.bz_price['sell']} SELL: {i.bz_price['sell']}")

    @commands.command()
    async def notify_me(self, ctx, item, above_below, price_per_item):
        pass


bot.run(config.GLOBAL_CONFIG["discord_token"])
