import discord
import requests
from discord.ext import commands
from datetime import datetime


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def purge(self, ctx, amount=None):
        if amount is None:
            if ctx.message.reference:
                async for msg in ctx.channel.history(limit=None):
                    if msg.author == self.client.user:
                        await msg.delete()
                    if (
                        msg.id == ctx.message.reference.message_id
                    ):  # once initial message is reached
                        return
        else:
            amount = int(amount)
            counter = -1
            async for msg in ctx.channel.history(limit=None):
                if counter >= amount:
                    return

                if msg.author == self.client.user:
                    await msg.delete()
                    counter += 1

    @commands.command()
    async def joinvc(self, ctx, id):
        await self.client.get_channel(int(id)).connect()

    @commands.command()
    async def fetch(self, ctx, id):
        if "<@" in id:
            id = id.strip("<@").strip(">")

        user = await self.client.fetch_user(int(id))
        msg = f"{user} - {user.id}\nAvatar URL: {user.avatar_url}\nJoin date: <t:{int(user.created_at.timestamp())}>"
        banner_request = await self.client.http.request(
            discord.http.Route("GET", f"/users/{id}")
        )
        if banner_request["banner"]:
            banner_url = f"https://cdn.discordapp.com/banners/{id}/{banner_request['banner']}?size=1024"
            msg += f"\nBanner URL: {banner_url}"

        await ctx.message.edit(content=msg)

    @commands.command()
    async def whatis(self, ctx, query):
        r = requests.get(
            f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={query}"
        )
        result = r.json()

        page = list(result["query"]["pages"].values())[0]

        ellipses = ""

        if "may refer to" not in page["extract"]:
            page["extract"] = page["extract"].replace("\n", "\n\n")
            ellipses = "..."

        await ctx.message.edit(
            content=f"""**{page["title"]}:**

{page["extract"][:1990 - len(page["title"])]}{ellipses}
"""
        )

    @commands.command(aliases=["wiki"])
    async def wikipedia(self, ctx, query):
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&namespace=0&format=json"
        ).json()
        results = "\n".join(
            [
                f"**{name}:** <{response[3][index]}>"
                for index, name in enumerate(response[1])
            ]
        )

        await ctx.message.edit(
            content=f"""Search results for \"{query}\"

{results}
"""
        )

    @commands.command()
    async def fakeuser(self, ctx, nationality=None):
        url = "https://randomuser.me/api/1.4"
        if nationality:
            url += f"?nat={nationality}"

        identity = requests.get(url).json()["results"][0]
        date_of_birth = int(
            datetime.fromisoformat(identity["dob"]["date"].rstrip("Z")).timestamp()
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


def setup(client):
    client.add_cog(Utility(client))
