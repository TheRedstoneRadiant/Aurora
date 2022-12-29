import json
import discord
from discord.ext import commands

STATUS_OPTIONS = ("idle", "invisible", "online", "dnd")


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def status(self, ctx, *, status):
        if status.lower() not in STATUS_OPTIONS:
            await ctx.message.edit(
                "Valid options: "
                + ", ".join(option.capitalize() for option in STATUS_OPTIONS)
            )

        config = {"status": status}
        with open("config.json") as file:
            json.dump(config, file)

        await self.client.change_presence(status=getattr(discord.Status, status))


def setup(client):
    client.add_cog(Config(client))
