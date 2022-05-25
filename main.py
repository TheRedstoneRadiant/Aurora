import discord, os

token = os.environ["token"]
client = discord.Client(guild_subscription_options=discord.GuildSubscriptionOptions.off())

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

if __name__ == "__main__":
    try:
        keep_alive()  # start replit webserver
        client.run(token)
    except discord.errors.HTTPException:
        os.system("kill 1")  # reset repl ip address