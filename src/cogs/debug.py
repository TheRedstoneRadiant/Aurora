import os
import sys
from io import StringIO
from discord.ext import commands

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from better_deleter import clear_guild_messages


class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(breif="Run Python code! Supports \`\`\`py formatting too <3")
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

    @commands.command(aliases=["abort", "quit"], breif="The literal defenition of \"kys\"")
    async def exit(self, ctx):
        await ctx.message.add_reaction("👍")
        os.system("kill 1")

    @commands.command(breif="Clears all of your messages in a server :trollface:")
    async def guildclear(self, ctx, user_id=None):
        if user_id is None:
            user_id = self.client.user.id

        await ctx.message.edit(content="Clearing messages...")
        await clear_guild_messages(os.environ["token"], str(ctx.guild.id), user_id)


def setup(client):
    client.add_cog(Debug(client))
