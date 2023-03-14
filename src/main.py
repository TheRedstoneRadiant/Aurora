import os
import sys
import discord
from utils.config import load_config
from discord.ext import commands
from webserver import start_webserver

config = load_config(os.path.join(os.getcwd(), "config.json"))

async def get_latest_prefix(bot, message):
    return [",", client.prefix_latest]


client = commands.Bot(
    self_bot=True,
    command_prefix=get_latest_prefix,
    case_insensitive=True,
    status=getattr(discord.Status, config.get("status", "idle")),
    guild_subscription_options=discord.GuildSubscriptionOptions.off(),
)

client.prefix_latest = config.get("prefix", ",")

cogs = ["cogs.utility", "cogs.debug", "cogs.meme", "cogs.config"]

if "CANVAS_TOKEN" in os.environ:
    cogs.append("cogs.canvas")  # enables canvas module


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    for cog in cogs:
        try:
            client.load_extension(cog)
            print(f"Loaded '{cog}'")

        except Exception as e:
            print(f"Error when loading {cog}\n{e}")


@client.event
async def on_raw_message_edit(payload):
    author = payload.data.get("author")

    if not author or author["id"] != str(client.user.id):
        return

    if payload.cached_message:  # message cached
        message = payload.cached_message

    else:  # fetch message
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

    if not message.content.startswith(client.command_prefix):
        return

    await client.process_commands(message)


try:
    stdout = sys.stdout
    f = open("log.txt", "w")
    sys.stdout = f
    
    if os.environ.get("REPLIT"):
        start_webserver()

    client.run(os.environ["TOKEN"])

finally:
    sys.stdout = stdout
    f.close()
