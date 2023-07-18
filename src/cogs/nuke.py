import random
import discord
from discord.ext import commands


class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_channel_members(ctx):
        # Guild text channel
        if isinstance(ctx.channel, discord.TextChannel):
            return ctx.channel.members
        
        # Direct Message
        elif isinstance(ctx.channel, discord.DMChannel):
            return [ctx.channel.recipient]
        
        # Groupchat
        elif isinstance(ctx.channel, discord.GroupChannel):
            return ctx.channel.recipients

    @commands.command(brief="Lists the amount of members in the current channel.", aliases=["mc"])
    async def membercount(self, ctx):
        members = self.get_channel_members(ctx)

        await ctx.message.edit(content=f"{len(members)} members")

    @commands.command(brief="Mass ping users in the current channel.", aliases=["mp"])
    async def massping(self, ctx, max_people_amount=None):
        members = self.get_channel_members(ctx)

        # Strip max people pinged
        if max_people_amount:
            members = members[:int(max_people_amount)]
        
        # Randomly shuffle members
        random.shuffle(members)

        pings = []
        for member in members:
            pings.append(member.mention)

        # Split into messages of 90 pings (2000 / 22)
        messages = []
        for i in range(0, len(pings), 90):
            messages.append("".join(pings[i : i + 90]))

        for message in messages:
            try:
                await ctx.channel.send(message, delete_after=0.00005)

            # Automod mention limits
            except discord.errors.HTTPException:
                await ctx.message.edit(content="Server blocked.")
                break

    @commands.command(brief="Spam a message automatically", aliases=["s"])
    async def spam(self, ctx, amount, message):
        for i in range(int(amount)):
            await ctx.channel.send(message)


def setup(client):
    client.add_cog(Nuke(client))
