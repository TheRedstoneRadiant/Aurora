import subprocess
import discord
import requests
from discord.ext import commands
from datetime import datetime
from utils.prop import Client

client = Client()


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        brief="Deletes a specific amount of messages in the current channel, or upto the message that you reply to"
    )
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

    @commands.command(brief="Same as ,purge but for every user (needs manage messages)")
    async def purgeall(self, ctx, amount=None):
        if amount is None:
            if ctx.message.reference:
                async for msg in ctx.channel.history(limit=None):
                    try:
                        await msg.delete()
                    except:
                        pass

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

                try:
                    await msg.delete()
                    counter += 1
                except:
                    pass

    @commands.command(brief="Fetches and joins a voice channel by ID")
    async def joinvc(self, ctx, id):
        await self.client.get_channel(int(id)).connect()

    @commands.command(brief="Lookup information about a Discord user")
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

    @commands.command(brief="Fetches wikipedia for a short summary of your query")
    async def whatis(self, ctx, *, query):
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

    @commands.command(
        aliases=["wiki"],
        brief="Lists out wikipedia articles that are relevant to your query",
    )
    async def wikipedia(self, ctx, *, query):
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

    @commands.command(brief="Useful little fake identity command for placeholder data")
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

    @commands.command(brief="Run Bash commands!")
    async def cmd(self, ctx, *, cmd):
        await ctx.message.edit(
            content=f"```\n{cmd}:\n\n{subprocess.check_output(cmd, shell=True).decode()[:1980]}\n```"
        )

    # @staticmethod
    # def parse_duration(duration):
    #     unit_multipliers = {
    #         's': 1,
    #         'm': 60,
    #         'h': 3600,
    #         'd': 86400,
    #         'w': 604800,
    #         'y': 31536000
    #     }

    #     match = re.match(r'(\d+)([smhdwy])', duration)
    #     if not match:
    #         return None

    #     num, unit = match.groups()
    #     num = int(num)
    #     return num * unit_multipliers[unit]

    @commands.command(
        aliases=["p", "paste"],
        brief="Creates a paste on a pastebin service with an optional expiration duration for the content. This command allows you to quickly share code or text with others by posting it to a pastebin and provides an option to set the duration of how long the paste should be available. The command also supports attaching files to the paste, and if no text is provided, it will use the content of the attached files. Use durations like '1s' for one second, '1m' for one minute, '1h' for one hour, '1d' for one day, '1w' for one week, or '1y' for one year. (NOTE: DURATION CURRENTLY BROKEY!)",
    )
    async def pastebin(
        self, ctx, *, text: str = None
    ):  # (self, ctx, duration: str = None, *, text: str = None):
        # if duration is None:
        # multiplier = 2592000
        # expire_seconds = 999

        # else:
        #     multiplier = 1

        #     # Parse the duration and convert to seconds
        #     expire_seconds = self.parse_duration(duration)
        #     if expire_seconds is None:
        # return await ctx.message.edit(content="Invalid duration format. Use '1s', '1m', '1h', '1d', '1w', or '1y'.")

        # Handle text parameter
        if text is None:
            if not ctx.message.attachments:
                return await ctx.message.edit(
                    content="Please attach files, or pass text parameter."
                )

            attachments_content = []
            for attachment in ctx.message.attachments:
                file_content = str(await attachment.read())[2:-1]
                attachments_content.append(
                    f"==== {attachment.filename} ====\n{file_content}"
                )

            text = "\n\n".join(attachments_content)

        url = "https://paste.fyi/?redirect"
        data = {"paste": text, "highlight": "", "expire": 999, "multiplier": 2592000}

        with requests.post(url, data=data) as response:
            if response.status_code == 200:
                pastebin_url = response.url
                await ctx.message.reply(content=f"**{pastebin_url}**")
            else:
                await ctx.message.edit(content="Failed to create paste.")

    @commands.command(brief="Search the web.", aliases=["q"])
    async def search(self, ctx, *, query):
        response = client.q(query)
        result = response["response"].replace("####", "##")
        if len(result) > 2000:
            await self.pastebin(ctx, text=result)

        else:
            await ctx.message.edit(content=result)


async def setup(client):
    await client.add_cog(Utility(client))
