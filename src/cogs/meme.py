import requests, random, discord, io
from discord.ext import commands


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        brief="Random image of an anime girl holding a programming book"
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
        
    @commands.command(brief="Generate a random XKCD comic")
    async def xkcd(self, ctx):
        latest_comic = requests.get("https://xkcd.com/info.0.json").json()
        latest_comic_number = latest_comic["num"]

        random_comic_num = random.randint(1, latest_comic_number)

        random_comic = requests.get(f"https://xkcd.com/{random_comic_num}/info.0.json").json()
        comic_img_url = random_comic["img"]

        await ctx.message.edit(content=comic_img_url)

    @commands.command(brief="Generate a random cute cat")
    async def cat(self, ctx):
        await ctx.message.edit(content=f"https://cataas.com/cat/cute?{random.randint(1,1000)}")


async def setup(client):
    await client.add_cog(Meme(client))
