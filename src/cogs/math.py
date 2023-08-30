import requests
import io
import discord
import json
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["w"],
        brief="Render math as LaTeX!",
    )
    async def latex(self, ctx, *, latex):
        response = requests.post(
            "http://latex2png.com/api/convert",
            data=json.dumps(
                {
                    "auth": {"user": "guest", "password": "guest"},
                    "latex": latex,
                    "resolution": 300,
                    "color": "ffffff",
                }
            ),
        )

        response = requests.get("http://latex2png.com" + response.json().get("url"))

        if response.status_code == 200:
            img = response.content

            with io.BytesIO(img) as file:
                await ctx.message.edit(
                    content=f"`{latex}`", attachments=[discord.File(file, "1.png")]
                )

        else:
            return await ctx.message.edit(
                content=f"Failed to fetch image: {response.status_code}"
            )


async def setup(client):
    await client.add_cog(Math(client))
