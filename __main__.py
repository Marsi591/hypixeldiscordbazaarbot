import discord
from discord.ext import commands, tasks
import math
import requests
import json

with open("config.json") as config:
    config_dict = json.load(config)
    HYPIXEL_API_KEY = config_dict["hypixel-key"]
    DISCORD_API_KEY = config_dict["discord-token"]

HYPIXEL_API_URL = 'https://api.hypixel.net/'

x = requests.get(HYPIXEL_API_URL + "key",params={"key":HYPIXEL_API_KEY})

print(x.json())

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$',intents=intents)

bazaar_data = None

@bot.event
async def on_ready():
    await bot.add_cog(BazaarCog(bot))

class BazaarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bazaar_data = None
        self.settings = {
            "margin":500,
        }
        self.updater.start()

    def cog_unload(self):
        self.updater.cancel()

    @commands.command()
    async def bz(self, ctx, arg):
        if self.bazaar_data["success"]:
            await ctx.send(f"""{arg}
        Buy Price: {self.bazaar_data["products"][arg]["quick_status"]["buyPrice"]:,} coins
        Sell Price: {self.bazaar_data["products"][arg]["quick_status"]["sellPrice"]:,} coins
        Sales in the past 7d: {self.bazaar_data["products"][arg]["quick_status"]["sellMovingWeek"]:,} 
            
        """)
        else:
            await ctx.send("<@211979681774174209> Something went wrong fetching bazaar data!")
    
    @commands.command()
    async def margin(self, ctx, ammount, t_type):
        if t_type=="percent":
            ctx.send(f"Set margin tracker to {ammount}% of the total price.")
        if t_type=="coins":
            ctx.send(f"Set margin tracker to {ammount}% coins.")

    @commands.command()
    async def spike(self, ctx, ammount, t_type):
        if t_type=="percent":
            ctx.send(f"Set spike tracker to {ammount}% of the total price.")
        if t_type=="coins":
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
        for i in list(self.bazaar_data["products"].keys()):
            quick_status = self.bazaar_data["products"][i]["quick_status"]
            margin = abs(quick_status["sellPrice"] - quick_status["buyPrice"])
            if margin > self.settings["margin"]:
                await ctx.send(f"{i} has a margin of {math.floor(margin)} coins.")
                await ctx.send(f"BUY: {quick_status['sellPrice']} SELL: {quick_status['sellPrice']}")
                break


    @commands.command()
    async def notify_me(self, ctx, item, above_below, price_per_item):
        pass

    @tasks.loop(seconds=120.0)
    async def updater(self):
        print("Updating bazaar data...")
        self.bazaar_data = requests.get(HYPIXEL_API_URL+"skyblock/bazaar").json()
        print(f"Success: {self.bazaar_data['success']}")

bot.run(DISCORD_API_KEY)

