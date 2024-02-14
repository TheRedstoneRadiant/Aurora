import os
import sys
from io import StringIO
from discord.ext import commands

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from better_deleter import clear_guild_messages


class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Run Python code! Supports code blocks.")
    async def eval(self, ctx, *, code):
        if "```" in code:
            code = code.replace("```py", "").replace("```", "").strip()

        message = await ctx.reply("output")

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            exec(code)
            await message.edit(content=redirected_output.getvalue())

        except Exception as e:
            await message.edit(content=e)

        finally:
            sys.stdout = old_stdout

    @commands.command(
        aliases=["abort", "quit"], brief='Turn off selfbot. Will cancel all running operations.'
    )
    async def exit(self, ctx):
        await ctx.message.add_reaction("👍")
        await self.client.close()

    @commands.command(brief="Deletes all of your messages in a server.", aliases=["gc"])
    async def guildclear(self, ctx, user_id=None):
        if user_id is None:
            user_id = self.client.user.id

        await ctx.message.edit(content="Clearing messages...")
        await clear_guild_messages(os.environ["TOKEN"], str(ctx.guild.id), user_id)


async def setup(client):
    await client.add_cog(Debug(client))
