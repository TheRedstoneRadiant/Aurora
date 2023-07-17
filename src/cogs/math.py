import requests
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["latex", "w"],
        brief="Deletes a specific amount of messages in the current channel, or upto the message that you reply to",
    )
    async def latex(self, ctx, latex):
        response = requests.post(
            "https://latex2png.com/api/convert",
            data={"auth":{"user":"guest","password":"guest"},"latex": latex, "resolution":600,"color":"000000"},
        )
        await ctx.message.edit(
            content="https://latex2png.com/" + response.json().get("url")
        )


def setup(client):
    client.add_cog(Math(client))
