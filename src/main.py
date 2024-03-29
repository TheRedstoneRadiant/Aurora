import os
import discord
from utils.config import load_config
from utils.logger import configure_logger
from discord.ext import commands

handler = configure_logger("discord_log.log")
config = load_config(os.path.join(os.getcwd(), "config.json"))


async def get_latest_prefix(_bot, _message):
    return [",", client.prefix_latest]


cogs = [
    "cogs.utility",
    "cogs.debug",
    "cogs.meme",
    "cogs.config",
    "cogs.math",
    "cogs.nuke",
    "cogs.ai",
]

if "CANVAS_TOKEN" in os.environ:
    cogs.append("cogs.canvas")  # enables canvas module


class MyClient(commands.Bot):
    async def setup_hook(self):
        # Load bot cogs
        for cog in cogs:
            try:
                await client.load_extension(cog)
                print(f"Loaded '{cog}'")

            except Exception as e:
                print(f"Error when loading {cog}\n{e}")


client = MyClient(
    self_bot=True,
    command_prefix=get_latest_prefix,
    case_insensitive=True,
    status=getattr(discord.Status, config.get("status", "invisible")),
    log_handler=handler,
    help_command=None,
)

client.prefix_latest = config.get("prefix", ",")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_command_error(ctx, error):
    print(f"An error occured: {str(error)}")  # Log Error

    try:
        await ctx.message.edit(content=f"An error occured: {str(error)}")
    except:
        pass


@client.command(aliases=["r", "reload"])
async def reload_cogs(ctx):
    for cog in cogs:
        try:
            await client.reload_extension(name=cog)
            print(f"Reloaded {cog}")
        except Exception as e:
            print(f"Error when reloading {cog}\n{e}")

    await ctx.message.edit(content="Reloaded cogs.")


if "LOGGER_WEBHOOK_URL" in os.environ:
    print(f"[!] Webhook message logging enabled.")

# Replit webserver
if "REPLIT" in os.environ:
    from webserver import start_webserver

    start_webserver()

client.run(os.environ["TOKEN"])
