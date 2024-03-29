import subprocess
import os
import discord
import requests
from discord.ext import commands
from datetime import datetime
from utils.prop import Client

client = Client()


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.snipe_cache = {}

    @commands.command(
        brief="Deletes a specific amount of messages in the current channel, or upto the message that you reply to",
        aliases=["p"],
    )
    async def purge(self, ctx, amount=None):
        if amount is None:
            if ctx.message.reference:
                async for msg in ctx.channel.history(limit=None):
                    if msg.author == self.client.user:
                        try:
                            await msg.delete()
                        except:
                            continue
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
                    try:
                        await msg.delete()
                    except:
                        continue

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
        msg = f"{user} - {user.id}\nAvatar URL: {user.avatar}\nJoin date: <t:{int(user.created_at.timestamp())}>"
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

    @commands.command(brief="Fake identity command for placeholder data")
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

    @commands.command(
        aliases=["paste"],
        brief="Creates a paste on a pastebin service with an optional expiration duration for the content. This command allows you to quickly share code or text with others by posting it to a pastebin and provides an option to set the duration of how long the paste should be available. The command also supports attaching files to the paste, and if no text is provided, it will use the content of the attached files. Use durations like '1s' for one second, '1m' for one minute, '1h' for one hour, '1d' for one day, '1w' for one week, or '1y' for one year. (NOTE: DURATION CURRENTLY BROKEY!)",
    )
    async def pastebin(self, ctx, *, text: str = None):
        # Handle text parameter
        if text is None:
            if not ctx.message.attachments:
                return await ctx.message.edit(
                    content="Please attach files, or pass text parameter."
                )

            ATTACH_FILE_HEADER = len(ctx.message.attachments) > 1

            attachments_content = []
            for attachment in ctx.message.attachments:
                file_content = str(await attachment.read())[2:-1].replace("\\n", "\n")
                filename_header = f"==== {attachment.filename} ====\n"
                attachments_content.append(
                    f"{filename_header if ATTACH_FILE_HEADER else ''}{file_content}"
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

    @commands.command(brief="Help command.")
    async def help(self, ctx):
        help_message = "Available commands:\n\n"

        for cog in self.client.cogs.values():
            cog_commands = cog.get_commands()
            if cog_commands:
                cog_name = cog.__class__.__name__
                commands = "\n".join(
                    f"{', '.join([str(command), *command.aliases])} - {command.brief[:65] if command.brief else ''}{'...' if command.brief and len(command.brief) > 65 else ''}"
                    for command in cog_commands
                )
                help_message += f"**{cog_name}:**\n{commands}\n\n"

        await ctx.message.edit(content=help_message)

    async def log_message(self, message, action):
        if (
            not os.environ.get("LOGGER_WEBHOOK_URL")
            or message.author == self.client.user
            or message.author.bot
            or (message.guild and message.guild.member_count > 1000)
        ):
            return

        if message.guild:
            guild_name = str(message.guild)
        else:
            guild_name = str(message.channel)

        embed = discord.Embed(
            type="rich", title=action, color=0xFF0000, timestamp=datetime.now()
        )

        if message.content:
            embed.add_field(name="Content", value=message.content, inline=False)

        if message.guild and message.guild.icon:
            embed.set_thumbnail(url=message.guild.icon.url)

        embed.set_footer(
            text=f"{str(message.author).replace('#0', '')} in {guild_name}",
            icon_url=message.author.avatar,
        )

        embed.add_field(name="Jump URL", value=message.jump_url, inline=False)
        embed.add_field(
            name="Creation Date",
            value=f"<t:{int(message.created_at.timestamp())}:R>",
            inline=False,
        )

        webhook = discord.SyncWebhook.from_url(os.environ["LOGGER_WEBHOOK_URL"])
        webhook.send(embeds=[embed], files=message.attachments)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.attachments:
            new_attachments = []

            for attachment in message.attachments:
                file_object = await attachment.to_file()
                new_attachments.append(file_object)

            message.attachments = new_attachments

        self.snipe_cache[message.channel.id] = message

        await self.log_message(message, action="Message Deleted")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.log_message(before, action="Message Edited")

    @commands.command(
        brief="Get the last deleted message in the current channel.", aliases=["s"]
    )
    async def snipe(self, ctx):
        latest_snipe = self.snipe_cache.get(ctx.channel.id)

        if latest_snipe:
            await ctx.message.edit(
                attachments=latest_snipe.attachments,
                content=f"**{str(latest_snipe.author).replace('#0', '')}**:\n{latest_snipe.content}",
            )

        else:
            await ctx.message.delete()

    @commands.command(brief="Close all DMs.", aliases=["cad", "closealldm"])
    async def closealldms(self, ctx):
        for channel in self.client.private_channels:
            if isinstance(channel, discord.DMChannel):
                await channel.close()

        await ctx.message.delete()


async def setup(client):
    await client.add_cog(Utility(client))
