import os
import json
import discord
from discord.ext import commands

STATUS_OPTIONS = ("idle", "invisible", "online", "dnd")


def create_config(payload):
    with open("config.json", "w") as file:
        json.dump({}, file)


def update_config(payload: dict):
    try:
        with open("config.json", "r+") as file:
            config = json.load(file)

            for key, value in payload.items():
                config[key] = value

            file.seek(0)
            json.dump(config, file)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        create_config(payload)


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

        update_config({"status": status})
        await self.client.change_presence(status=getattr(discord.Status, status))

    @commands.command()
    async def prefix(self, ctx, *, prefix):
        update_config({"prefix": prefix})


def setup(client):
    client.add_cog(Config(client))
