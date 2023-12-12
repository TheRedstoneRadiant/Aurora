import aiohttp
from discord.ext import commands
from utils.prop import Client

client = Client()


class AI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_url = "https://gpti.projectsrpp.repl.co/api"

    async def fetch_image(self, prompt):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/dalleai", json={"prompt": prompt, "type": "json"}
            ) as response:
                return await response.json()

    @commands.command(brief="Generates an AI image using DALL-E")
    async def dalle(self, ctx: commands.Context, *, prompt: str):
        await ctx.message.edit(
            content=f"**Generating image via DALL-E...**\n**`{prompt}`**"
        )

        try:
            image = await self.fetch_image(prompt)
            if image.get("code") == 200:
                await self.client.cogs["Meme"].send_random_image(
                    ctx=ctx,
                    url=image["ul"],
                    filename="0.png",
                    content=f"**`{prompt}`**",
                )
            else:
                await ctx.message.edit(
                    content=f"{image['code']} error during generation: '{image['message']}'"
                )
        except Exception as e:
            await ctx.message.edit(
                content=f"An error occurred during image generation: {str(e)}"
            )


async def setup(client):
    await client.add_cog(AI(client))
