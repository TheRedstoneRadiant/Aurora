import os
import json
import discord
from discord.ext import commands

# Define possible status options
STATUS_OPTIONS = ("idle", "invisible", "online", "dnd")


class Config(commands.Cog):
    """
    A cog for handling configuration commands.
    """

    def __init__(self, client: commands.Bot):
        """
        Initialize the Config cog.

        Args:
            client (commands.Bot): The Discord bot client.
        """
        self.client = client

    @commands.command(brief="Set the Discord status (idle, dnd, online, offline).")
    async def status(self, ctx: commands.Context, *, status: str):
        """
        Set the bot's Discord status.

        Args:
            ctx (commands.Context): The command context.
            status (str): The desired status.

        Example:
            !status online
        """
        status = status.lower()

        # Handle "invis" or "invisible" as "offline"
        if status in ("invis", "offline"):
            status = "invisible"

        if status not in STATUS_OPTIONS:
            return await ctx.send(
                f"Valid options: {', '.join(option.capitalize() for option in STATUS_OPTIONS)}"
            )

        await self.client.change_presence(status=getattr(discord.Status, status))

    @commands.command(
        brief="Change the bot prefix. You can set a custom prefix alongside ',' (default)."
    )
    async def prefix(self, ctx: commands.Context, *, prefix: str):
        """
        Change the bot's command prefix.

        Args:
            ctx (commands.Context): The command context.
            prefix (str): The new prefix.

        Example:
            ,prefix !
        """
        update_config({"prefix": prefix})

        # Update prefix
        self.client.prefix_latest = prefix

        await ctx.message.edit(content=f'Prefix updated. Your prefix is now "{prefix}".')


def update_config(payload: dict):
    """
    Update the configuration file with new values.

    Args:
        payload (dict): The dictionary of configuration values to update.
    """
    with open("config.json", "r") as file:
        config = json.load(file)

    with open("config.json", "w") as file:
        for key, value in payload.items():
            config[key] = value

        json.dump(config, file)


async def setup(client: commands.Bot):
    """
    Add the Config cog to the bot.

    Args:
        client (commands.Bot): The Discord bot client.
    """
    await client.add_cog(Config(client))
