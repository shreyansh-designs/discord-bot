import discord
from discord.ext import commands
import platform

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):

        latency = round(self.bot.latency * 1000)

        await ctx.send(
            f"🏓 Pong! `{latency}ms`"
        )

    @commands.command()
    async def helpme(self, ctx):

        embed = discord.Embed(
            title="🤖 Katalyst Commands",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🌱 Onboarding",
            value=(
                "`!setup`\n"
                "`!profile`\n"
                "`!leaderboard`"
            ),
            inline=False
        )

        embed.add_field(
            name="⚡ Utility",
            value=(
                "`!ping`\n"
                "`!botinfo`"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):

        embed = discord.Embed(
            title="🤖 Katalyst",
            description="Community onboarding bot",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Python",
            value=platform.python_version()
        )

        embed.add_field(
            name="Servers",
            value=str(len(self.bot.guilds))
        )

        await ctx.send(embed=embed)

async def setup(bot):

    await bot.add_cog(
        Utility(bot)
    )
