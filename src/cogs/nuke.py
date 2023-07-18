import random
import discord
from discord.ext import commands


class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Lists the amount of members in the current channel.", aliases=["mc"])
    async def membercount(self, ctx):
        await ctx.message.edit(content=f"{len(ctx.channel.members)} members")

    @commands.command(brief="Mass ping users in the current channel.", aliases=["mp"])
    async def massping(self, ctx, max_people_amount=9999):
        members = ctx.channel.members[:int(max_people_amount)]
        random.shuffle(members)

        pings = []
        for member in members:
            pings.append(member.mention)

        messages = []
        for i in range(0, len(pings), 90):
            messages.append("".join(pings[i : i + 90]))

        for message in messages:
            try:
                await ctx.channel.send(message, delete_after=0.00005)
            except discord.errors.HTTPException:
                await ctx.message.edit(content="Server blocked.")
                break


def setup(client):
    client.add_cog(Nuke(client))
