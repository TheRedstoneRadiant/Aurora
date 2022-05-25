import discord, os
from discord.ext import commands

token = os.environ["token"]
client = commands.Bot(self_bot=True, command_prefix=",", case_insensitive=True)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

if __name__ == "__main__":
    keep_alive()  # start replit webserver
    try:
        client.run(token)
    except discord.errors.HTTPException:
        os.system("kill 1")  # reset repl ip address