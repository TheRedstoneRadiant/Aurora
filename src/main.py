import os
import discord
import json
from discord.ext import commands

BOT_PREFIX = ","
BOT_STATUS = "idle"

if "config.json" in os.listdir:
    with open("config.json") as file:
        config = json.load(file)

    BOT_PREFIX = config.get("prefix", BOT_PREFIX)
    BOT_STATUS = config.get("status", BOT_STATUS)

client = commands.Bot(
    self_bot=True,
    command_prefix=BOT_PREFIX,
    case_insensitive=True,
    status=getattr(discord.Status, BOT_STATUS),
    guild_subscription_options=discord.GuildSubscriptionOptions.off(),
)

cogs = ["cogs.utility", "cogs.debug", "cogs.meme"]

if os.environ.get("VLC_TOKEN"):
    cogs.append("cogs.vlc")


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


client.run(os.environ["TOKEN"])
