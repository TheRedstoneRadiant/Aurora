import aiohttp
from discord.ext import commands
from utils.prop import Client

client = Client()


class AI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_url = "https://gpti.projectsrpp.repl.co/api"

    async def make_api_request(self, request_url, json):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=request_url, json=json) as response:
                return await response.json()

    @commands.command(brief="Generates an AI image using DALL-E", aliases=["img"])
    async def dalle(self, ctx: commands.Context, *, prompt: str):
        await ctx.message.edit(
            content=f"**Generating image via DALL-E...**\n**`{prompt}`**"
        )

        try:
            image = await self.make_api_request(
                f"{self.api_url}/dalleai", {"prompt": prompt, "type": "json"}
            )
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

    @commands.command(brief="Ask GPT4 a question!", aliases=["gpt", "ask"])
    async def gpt4(self, ctx: commands.Context, *, prompt: str):
        await ctx.message.edit(content=f"**🤔 Thinking...**\n**`{prompt}`**")

        try:
            response = await self.make_api_request(
                f"{self.api_url}/gpti", {"prompt": prompt, "type": "json", "model": "1"}
            )
            if response.get("code") == 200:
                await ctx.message.edit(content=f"**`{prompt}`**\n{response['gpt']}")
            else:
                await ctx.message.edit(
                    content=f"{response['code']} error during generation: '{response['message']}'"
                )
        except Exception as e:
            await ctx.message.edit(
                content=f"An error occurred during image generation: {str(e)}"
            )


async def setup(client):
    await client.add_cog(AI(client))
