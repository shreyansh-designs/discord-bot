import discord
import platform
from datetime import datetime

from discord.ext import commands

# ======================================================
# UTILITY COG
# ======================================================

class Utility(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # ==================================================
    # PING COMMAND
    # ==================================================

    @commands.command()

    async def ping(self, ctx):

        latency = round(
            self.bot.latency * 1000
        )

        embed = discord.Embed(
            title="🏓 Pong!",
            description=(
                f"Latency: `{latency}ms`"
            ),
            color=discord.Color.green()
        )

        embed.set_footer(
            text="KATALYST Utility System"
        )

        await ctx.send(embed=embed)

    # ==================================================
    # HELP COMMAND
    # ==================================================

    @commands.command()

    async def helpme(self, ctx):

        embed = discord.Embed(
            title="🤖 KATALYST COMMANDS",
            description=(
                "Community onboarding + "
                "XP + leveling system"
            ),
            color=discord.Color.blurple()
        )

        # ==============================================
        # ONBOARDING
        # ==============================================

        embed.add_field(
            name="🌱 Onboarding",
            value=(
                "`k!setup`\n"
                "`k!roles`\n"
                "`k!profile`\n"
                "`k!rank`\n"
                "`k!xp`\n"
                "`k!leaderboard`"
            ),
            inline=False
        )

        # ==============================================
        # UTILITY
        # ==============================================

        embed.add_field(
            name="⚡ Utility",
            value=(
                "`k!ping`\n"
                "`k!botinfo`\n"
                "`k!servers`\n"
                "`k!alive`\n"
                "`k!latency`"
            ),
            inline=False
        )

        # ==============================================
        # COMMUNITY
        # ==============================================

        embed.add_field(
            name="🎯 Community",
            value=(
                "💻 Programming\n"
                "🤖 AI / ML\n"
                "🛡️ Cybersecurity\n"
                "🧠 Psychology\n"
                "📈 Markets\n"
                "🚀 Startups"
            ),
            inline=False
        )

        embed.set_footer(
            text="KATALYST Community System"
        )

        await ctx.send(embed=embed)

    # ==================================================
    # BOT INFO
    # ==================================================

    @commands.command()

    async def botinfo(self, ctx):

        uptime = datetime.utcnow()

        embed = discord.Embed(
            title="🤖 KATALYST",
            description=(
                "Advanced Discord onboarding "
                "and community management bot."
            ),
            color=discord.Color.green()
        )

        embed.add_field(
            name="🐍 Python",
            value=platform.python_version(),
            inline=True
        )

        embed.add_field(
            name="📦 Discord.py",
            value=discord.__version__,
            inline=True
        )

        embed.add_field(
            name="🌍 Servers",
            value=str(
                len(self.bot.guilds)
            ),
            inline=True
        )

        embed.add_field(
            name="👥 Users",
            value=str(
                len(self.bot.users)
            ),
            inline=True
        )

        embed.add_field(
            name="⚡ Latency",
            value=(
                f"{round(self.bot.latency * 1000)}ms"
            ),
            inline=True
        )

        embed.add_field(
            name="🕒 UTC Time",
            value=uptime.strftime(
                "%H:%M:%S"
            ),
            inline=True
        )

        embed.set_footer(
            text="KATALYST System Monitor"
        )

        await ctx.send(embed=embed)

    # ==================================================
    # SERVER COUNT
    # ==================================================

    @commands.command()

    async def servers(self, ctx):

        await ctx.send(
            f"🌍 Connected Servers: "
            f"`{len(self.bot.guilds)}`"
        )

    # ==================================================
    # LATENCY COMMAND
    # ==================================================

    @commands.command()

    async def latency(self, ctx):

        latency = round(
            self.bot.latency * 1000
        )

        await ctx.send(
            f"⚡ Current latency: "
            f"`{latency}ms`"
        )

    # ==================================================
    # ALIVE COMMAND
    # ==================================================

    @commands.command()

    async def alive(self, ctx):

        embed = discord.Embed(
            title="✅ KATALYST ONLINE",
            description=(
                "Bot is online and operational."
            ),
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

# ======================================================
# SETUP
# ======================================================

async def setup(bot):

    await bot.add_cog(
        Utility(bot)
    )
