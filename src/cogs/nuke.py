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
    async def massping(
        self, ctx, mention_limit: int = 20, message_count: int = 3, members=None
    ):
        if members is None:
            members = self.get_channel_members(ctx)

        await ctx.message.delete()

        pings = []
        for member in members:
            pings.append(member.mention)

        # Send pings
        for i in range(message_count):
            try:
                # Randomly shuffle members
                random.shuffle(pings)

                message = "".join(pings[:mention_limit])
                await ctx.channel.send(message, delete_after=0.00005)

            # Automod mention limits
            except discord.errors.HTTPException:
                return await self.massping(
                    ctx, mention_limit // 2, message_count, members
                )

    @commands.command(brief="Spam a message automatically", aliases=["sp"])
    async def spam(self, ctx, amount, *, message):
        await ctx.message.delete()
        for i in range(0, int(amount)):  # amount - 1
            await ctx.channel.send(message)

    @commands.command(brief="Query guild members", aliases=["fm"])
    async def fetchmembers(self, ctx):
        await ctx.guild.fetch_members(channels=ctx.guild.channels)
        await ctx.message.delete()


async def setup(client):
    await client.add_cog(Nuke(client))
