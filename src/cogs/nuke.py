import random
import discord
from discord.ext import commands


class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_channel_members(self, ctx):
        # Guild text channel
        if isinstance(ctx.channel, discord.TextChannel):
            return ctx.channel.members

        # Direct Message
        elif isinstance(ctx.channel, discord.DMChannel):
            return [ctx.channel.recipient, ctx.message.author]

        # Groupchat
        elif isinstance(ctx.channel, discord.GroupChannel):
            return ctx.channel.recipients

    @commands.command(
        brief="Lists the amount of members in the current channel.", aliases=["mc"]
    )
    async def membercount(self, ctx):
        members = self.get_channel_members(ctx)

        await ctx.message.edit(content=f"{len(members)} members")

    @commands.command(brief="Mass ping users in the current channel.", aliases=["mp"])
    async def massping(self, ctx, message_count: int = 3, mention_limit: int = 20):
        members = self.get_channel_members(ctx)

        # Randomly shuffle members
        random.shuffle(members)

        pings = []
        for member in members:
            pings.append(member.mention)

        # Split into messages
        messages = []
        for i in range(0, message_count, mention_limit):
            messages.append("".join(pings[i : i + mention_limit]))

        for message in messages:
            try:
                await ctx.channel.send(message, delete_after=0.00005)

            # Automod mention limits
            except discord.errors.HTTPException:
                await ctx.message.delete()
                break

    @commands.command(brief="Spam a message automatically", aliases=["s"])
    async def spam(self, ctx, amount, *, message):
        for i in range(int(amount)):
            await ctx.channel.send(message)


def setup(client):
    client.add_cog(Nuke(client))
