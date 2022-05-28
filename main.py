import discord, json
from discord.ext import commands
from webserver import start_webserver

with open("config.json") as file:
    config = json.load(file)

token = os.environ["token"]
client = commands.Bot(
    command_prefix=config["prefix"],
    status=getattr(discord.Status, config["status"]),
    self_bot=True,
    case_insensitive=True
)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.command()
async def purge(ctx, amount=None):
    if not amount:
        return await ctx.message.edit("Usage: ,purge <amount>")

    async for message in ctx.channel.history(limit=None):
        if amount == 0:
            return

        if message.author == client.user:
            try:
                await message.delete()

            except discord.errors.Forbidden:
                continue

            amount -= 1




if __name__ == "__main__":
    start_webserver()  # start replit webserver
    try:
        client.run(token)
    except discord.errors.HTTPException:
        os.system("kill 1")  # reset repl ip address