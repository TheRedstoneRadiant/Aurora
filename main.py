import discord, json, requests, datetime, os
from discord.ext import commands
from webserver import start_webserver

with open("config.json") as file:
    config = json.load(file)

token = os.environ["token"]
client = commands.Bot(
    command_prefix=config["prefix"],
    status=getattr(discord.Status, config["status"]),
    self_bot=True,
    case_insensitive=True,
)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.command()
async def purge(ctx, amount=None):
    if not amount:
        return await ctx.message.edit("Usage: ,purge <amount>")

    async for message in ctx.channel.history(limit=None):
        if message.author == client.user:
            try:
                await message.delete()

            except discord.errors.Forbidden:
                continue

            amount -= 1

        if amount == 0:
            return


@client.command()
async def generateuser(ctx, nationality=None):
    url = "https://randomuser.me/api/1.4"
    if nationality:
        url += f"?nat={nationality}"

    identity = requests.get(url).json()["results"][0]
    date_of_birth = int(
        datetime.datetime.fromisoformat(identity["dob"]["date"].rstrip("Z")).timestamp()
    )

    return await ctx.message.edit(
        content=f"""
{identity["name"]["title"]}. {identity["name"]["first"]} {identity["name"]["last"]}
{identity["location"]["city"]}, {identity["location"]["state"]}, {identity["location"]["country"]}
{identity["location"]["street"]["number"]} {identity["location"]["street"]["name"]}, {identity["location"]["postcode"]}

Born <t:{date_of_birth}:R> on <t:{date_of_birth}>

Email: {identity["email"]}
Username: {identity["login"]["username"]}
Password: {identity["login"]["password"]}

{identity["picture"]["large"]}
"""
    )


if __name__ == "__main__":
    start_webserver()  # start replit webserver
    try:
        client.run(token)
    except discord.errors.HTTPException:
        os.system("kill 1")  # reset repl ip address
