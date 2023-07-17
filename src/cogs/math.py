import requests
import json
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["w"],
        brief="Render math as LaTeX!",
    )
    async def latex(self, ctx, latex):
        response = requests.post(
            "http://latex2png.com/api/convert",
            data=json.dumps(
                {
                    "auth": {"user": "guest", "password": "guest"},
                    "latex": latex,
                    "resolution": 600,
                    "color": "000000",
                }
            ),
        )
        await ctx.message.edit(
            content="http://latex2png.com" + response.json().get("url")
        )


def setup(client):
    client.add_cog(Math(client))
