embed = discord.Embed(
    title="Bazaar Sell",
    color=0xb05b48
)
embed.set_author(
    name=ctx.author.display_name,
    icon_url=ctx.author.avatar_url
)
embed.add_field(
    name=field1,
    value=value1,
    inline=False
)
embed.add_field(
    name=field2,
    value=value2,
    inline=False
)
embed.set_footer(
    text=ctx.created_at
)
