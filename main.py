import discord, json
from discord.ext import commands

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

if __name__ == "__main__":
    keep_alive()  # start replit webserver
    try:
        client.run(token)
    except discord.errors.HTTPException:
        os.system("kill 1")  # reset repl ip address