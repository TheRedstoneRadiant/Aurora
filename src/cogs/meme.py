import requests
import random
from discord.ext import commands


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(breif="https://github.com.cat-milk/Anime-Girls-Holding-Programming-Books Self explanatory")
    async def programmingbook(self, ctx):
        language = random.choice(
            requests.get(
                "https://api.github.com/repos/cat-milk/Anime-Girls-Holding-Programming-Books/contents"
            ).json()
        )
        image = random.choice(requests.get(language["url"]).json())
        print(ctx.message.content)
        await ctx.message.edit(
            content=f"""{image["download_url"]}

**{language["name"]}**:"""
        )


def setup(client):
    client.add_cog(Meme(client))
