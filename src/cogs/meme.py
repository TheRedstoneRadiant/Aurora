import random
import discord
import requests
import io
from discord.ext import commands
from typing import Optional


class Meme(commands.Cog):
    def __init__(self, client: commands.Bot):
        """
        Initializes the Meme Cog.

        Args:
            client (commands.Bot): The Discord bot client.
        """
        self.client = client
        self.api_url = "https://api.github.com/repos/cat-milk/Anime-Girls-Holding-Programming-Books/contents"
        self.xkcd_url = "https://xkcd.com/info.0.json"
        self.cute_cat_url = "https://cataas.com/cat/cute"
        self.random_user_agent = str(
            random.randint(1, 9)) * random.randint(10, 90)

    async def edit_message_with_image(
        self,
        ctx: commands.Context,
        content: str,
        image_url: str,
        file: Optional[discord.File] = None,
    ):
        """
        Edits a message in a channel, updating its content and/or attachments.

        Args:
            ctx (commands.Context): The context of the message.
            content (str): The new content of the message.
            image_url (str): URL of the image.
            file (discord.File, optional): The new attachment file. Defaults to None.
        """
        if file:
            await ctx.message.edit(content=content, attachments=[file])
        else:
            await ctx.message.edit(content=f"Failed to fetch image from <{image_url}>.")

    async def fetch_image(self, url: str, filename: str) -> Optional[discord.File]:
        """
        Fetches an image from a URL and returns it as a discord.File.

        Args:
            url (str): URL of the image to fetch.
            filename (str): Desired filename for the image.

        Returns:
            discord.File or None: The image as a discord.File if successful, else None.
        """
        response = requests.get(url)
        if response.status_code == 200:
            img = response.content
            file = discord.File(io.BytesIO(img), filename)
            return file

    async def send_random_image(
        self, ctx: commands.Context, url: str, filename: str, content: str
    ):
        """
        Sends a message with a random image and brief description.

        Args:
            ctx (commands.Context): The context of the message.
            url (str): URL of the image.
            filename (str): Filename for the image.
            content (str): The new content of the message.
        """
        image_url = url
        file = await self.fetch_image(image_url, filename)

        # Sending the message with image and description
        await self.edit_message_with_image(
            ctx=ctx,
            content=content,
            image_url=image_url,
            file=file,
        )

    @commands.command(brief="Random image of an anime girl with a programming book")
    async def programmingbook(self, ctx: commands.Context):
        """
        Sends a random image of an anime girl holding a programming book.

        Args:
            ctx (commands.Context): The context of the message.
        """
        # Fetching folders from the API response
        folders = [
            path["name"]
            for path in requests.get(self.api_url).json()
            if path["type"] == "dir"
        ]

        # Choosing a random language folder
        language_folder = random.choice(folders)

        # Fetching images in the chosen folder
        language_images = requests.get(
            f"{self.api_url}/{language_folder}").json()

        # Choosing a random image from the images
        image = random.choice(language_images)
        image_url = image["download_url"]

        # Sending the random image with description
        await self.send_random_image(
            ctx=ctx,
            url=image_url,
            filename="programming_book.png",
            content=f"**{language_folder.replace('-', ' ').title()}**:",
        )

    @commands.command(brief="Random XKCD comic")
    async def xkcd(self, ctx: commands.Context):
        """
        Sends a random XKCD comic along with its title and alt text.

        Args:
            ctx (commands.Context): The context of the message.
        """
        # Fetching information about the latest XKCD comic
        latest_comic = requests.get(self.xkcd_url).json()
        latest_comic_number = latest_comic["num"]

        # Choosing a random comic number
        random_comic_num = random.randint(1, latest_comic_number)
        random_comic = requests.get(
            f"https://xkcd.com/{random_comic_num}/info.0.json"
        ).json()
        image_url = random_comic["img"]

        # Sending the random comic with title and alt text
        await self.send_random_image(
            ctx=ctx,
            url=image_url,
            filename=f"xkcd_{random_comic_num}.png",
            content=f"**{random_comic['title']} (XKCD #{random_comic_num}):**\n{random_comic['alt']}",
        )

    @commands.command(brief="Random cute cat")
    async def cat(self, ctx: commands.Context):
        """
        Sends a random image of a cute cat.

        Args:
            ctx (commands.Context): The context of the message.
        """
        # Sending a random cute cat image
        await self.send_random_image(
            ctx=ctx, url=self.cute_cat_url, filename="cute_cat.png", content=""
        )

    @commands.command(brief="Random meme from r/memes")
    async def meme(self, ctx: commands.Context):
        fetched_meme = requests.get("https://meme-api.com/gimme/memes").json()
        await self.send_random_image(
            ctx=ctx,
            url=fetched_meme["url"],
            filename="meme.png",
            content=f'[Post Link](<{fetched_meme["postLink"]}>)\n**{fetched_meme["title"]}**',
        )

    @commands.command(brief="Fetch a random image from any subreddit")
    async def reddit(self, ctx: commands.Context, subreddit: str):
        fetched_post = requests.get(
            f"https://meme-api.com/gimme/{subreddit}").json()
        await self.send_random_image(
            ctx=ctx,
            url=fetched_post["url"],
            filename="meme.png",
            content=f'[Post Link](<{fetched_post["postLink"]}>)\n**{fetched_post["title"]}**',
        )


async def setup(client: commands.Bot):
    """
    Initializes the Meme cog and adds it to the client.

    Args:
        client (commands.Bot): The Discord bot client.
    """
    await client.add_cog(Meme(client))
