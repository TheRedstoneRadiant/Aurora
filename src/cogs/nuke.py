from discord.ext import commands


class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(breif="Lists the amount of members in the current channel.")
    async def membercount(self, ctx):
        await ctx.message.edit(content=f"{len(ctx.channel.members)} members")
        await ctx.message.delete()

    @commands.command(breif="Mass ping users in the current channel.")
    async def massping(self, ctx, max_people_amount):
        await ctx.message.delete()

        pings = []
        for member in ctx.channel.members[:max_people_amount]:
            pings.append(member.mention)

        messages = []
        for i in range(0, len(pings), 90):
            messages.append("".join(pings[i : i + 90]))

        for message in messages:
            await ctx.channel.send(message, delete_after=0.00005)


def setup(client):
    client.add_cog(Nuke(client))
