import requests, random, discord, io
from discord.ext import commands


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        brief="https://github.com.cat-milk/Anime-Girls-Holding-Programming-Books Self explanatory"
    )
    async def programmingbook(self, ctx):
        folders = [
            path
            for path in requests.get(
                "https://api.github.com/repos/cat-milk/Anime-Girls-Holding-Programming-Books/contents"
            ).json()
            if path["type"] == "dir"  # Directories only
        ]

        # Choose a random language folder
        language_folder = random.choice(folders)

        # Fetch images in the folder
        language_images = requests.get(language_folder["url"]).json()

        # Choose a random image out of the images
        image = random.choice(language_images)


        response = requests.get(image["download_url"])
        
        if response.status_code == 200:
            img = response.content

            with io.BytesIO(img) as file:
                await ctx.message.edit(
                    content=f'**{language_folder["name"]}**:', attachments=[discord.File(file, "1.png")]
                )

        else:
            return await ctx.message.edit(
                content=f"Failed to fetch image: {response.status_code}"
            )


async def setup(client):
    await client.add_cog(Meme(client))
