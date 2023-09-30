import requests
import io
import discord
import json
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.LATEX_API_URL = "https://rtex.probablyaweb.site/api/v2"
        self.LATEX_TEMPLATE = r"""
\documentclass{article}
\usepackage{amsmath,amsthm,amssymb,amsfonts}
\usepackage{bm}  % nice bold symbols for matrices and vectors
\usepackage{bbm}  % bold and calligraphic numbers
\usepackage[binary-units=true]{siunitx}  % SI unit handling
\usepackage{tikz}  % from here on, to make nice diagrams with tikz
\usepackage{ifthen}
\usetikzlibrary{patterns}
\usetikzlibrary{shapes, arrows, chains, fit, positioning, calc, decorations.pathreplacing}
\color{white}      % Set the default text color to white

\begin{document}
    \pagenumbering{gobble}
    $text
\end{document}"""

    @commands.command(
        aliases=["w"],
        brief="Render math as LaTeX!",
    )
    async def latex(self, ctx, *, latex):
        response = requests.post(
            self.LATEX_API_URL,
            data={
                "code": self.LATEX_TEMPLATE.replace("$text", latex),
                "format": "png",
            },
        )
        print(response.text)

        filename = response.json().get("filename")
        if not filename:
            response.status_code = 500

        response = requests.get(f"{self.LATEX_API_URL}/{filename}")
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
