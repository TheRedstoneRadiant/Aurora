import os
import json
import discord
from discord.ext import commands

STATUS_OPTIONS = ("idle", "invisible", "online", "dnd")


def update_config(payload: dict):
    with open("config.json", "r") as file:
        config = json.load(file)

    with open("config.json", "w") as file:
        for key, value in payload.items():
            config[key] = value

        json.dump(config, file)


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Set Discord status (idle, dnd, online, offline)")
    async def status(self, ctx, *, status):
        status = status.lower()
        if status not in STATUS_OPTIONS:
            return await ctx.message.edit(
                content="Valid options: "
                + ", ".join(option.capitalize() for option in STATUS_OPTIONS)
            )

        update_config({"status": status})

        # Update status
        await self.client.change_presence(status=getattr(discord.Status, status))

        # Success message
        await ctx.message.edit(content="Status updated.")

    @commands.command(
        brief='Change the bot prefix! You can set a custom prefix alongside "," (default)'
    )
    async def prefix(self, ctx, *, prefix):
        update_config({"prefix": prefix})

        # Update prefix
        self.client.prefix_latest = prefix

        await ctx.message.edit(
            content=f'Prefix updated. Your prefix is now "{prefix}".'
        )


async def setup(client):
    await client.add_cog(Config(client))
