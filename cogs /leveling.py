import discord
from discord.ext import commands
import json
import os

# ======================================================
# XP FILE
# ======================================================

XP_FILE = "data/xp.json"

# ======================================================
# CREATE DATA FOLDER
# ======================================================

if not os.path.exists("data"):

    os.makedirs("data")

# ======================================================
# CREATE XP FILE
# ======================================================

if not os.path.exists(XP_FILE):

    with open(XP_FILE, "w") as f:

        json.dump({}, f)

# ======================================================
# LOAD XP
# ======================================================

try:

    with open(XP_FILE, "r") as f:

        user_xp = json.load(f)

except:

    user_xp = {}

# ======================================================
# RANK SYSTEM
# ======================================================

RANKS = {
    0: "🌱 New Joiner",
    100: "🧠 Novice",
    300: "⚡ Skilled",
    700: "🔥 Advanced",
    1200: "👑 Supreme",
    2000: "💎 Ultimate"
}

# ======================================================
# SAVE XP
# ======================================================

def save_xp():

    try:

        with open(XP_FILE, "w") as f:

            json.dump(user_xp, f)

    except Exception as e:

        print(f"❌ XP Save Error: {e}")

# ======================================================
# GET RANK
# ======================================================

def get_rank(xp):

    current_rank = "🌱 New Joiner"

    for required_xp, rank_name in sorted(RANKS.items()):

        if xp >= required_xp:

            current_rank = rank_name

    return current_rank

# ======================================================
# LEVELING COG
# ======================================================

class Leveling(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # ==================================================
    # XP SYSTEM
    # ==================================================

    @commands.Cog.listener()

    async def on_message(self, message):

        if message.author.bot:
            return

        user_id = str(message.author.id)

        if user_id not in user_xp:

            user_xp[user_id] = 0

        # ==============================================
        # ADD XP
        # ==============================================

        user_xp[user_id] += 5

        save_xp()

        # ==============================================
        # PROCESS COMMANDS
        # IMPORTANT
        # ==============================================

        await self.bot.process_commands(message)

    # ==================================================
    # PROFILE COMMAND
    # ==================================================

    @commands.command()

    async def profile(self, ctx):

        user_id = str(ctx.author.id)

        xp = user_xp.get(user_id, 0)

        rank = get_rank(xp)

        embed = discord.Embed(
            title=f"👤 {ctx.author.name}",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(
            url=ctx.author.display_avatar.url
        )

        embed.add_field(
            name="⚡ XP",
            value=str(xp),
            inline=True
        )

        embed.add_field(
            name="🏆 Rank",
            value=rank,
            inline=True
        )

        embed.set_footer(
            text="KATALYST Level System"
        )

        await ctx.send(embed=embed)

    # ==================================================
    # RANK COMMAND
    # ==================================================

    @commands.command()

    async def rank(self, ctx):

        user_id = str(ctx.author.id)

        xp = user_xp.get(user_id, 0)

        rank = get_rank(xp)

        await ctx.send(
            f"🏆 {ctx.author.mention}\n"
            f"Rank: **{rank}**\n"
            f"XP: **{xp}**"
        )

    # ==================================================
    # XP COMMAND
    # ==================================================

    @commands.command()

    async def xp(self, ctx):

        user_id = str(ctx.author.id)

        xp = user_xp.get(user_id, 0)

        await ctx.send(
            f"⚡ {ctx.author.mention} has `{xp} XP`"
        )

    # ==================================================
    # LEADERBOARD COMMAND
    # ==================================================

    @commands.command()

    async def leaderboard(self, ctx):

        sorted_users = sorted(
            user_xp.items(),
            key=lambda x: x[1],
            reverse=True
        )

        embed = discord.Embed(
            title="🏆 KATALYST Leaderboard",
            color=discord.Color.gold()
        )

        leaderboard_text = ""

        for index, (user_id, xp) in enumerate(
            sorted_users[:10],
            start=1
        ):

            user = self.bot.get_user(int(user_id))

            if user:

                leaderboard_text += (
                    f"**{index}.** "
                    f"{user.name} — "
                    f"`{xp} XP` — "
                    f"{get_rank(xp)}\n"
                )

        if leaderboard_text == "":

            leaderboard_text = (
                "No active users yet."
            )

        embed.description = leaderboard_text

        embed.set_footer(
            text="Top Community Members"
        )

        await ctx.send(embed=embed)

# ======================================================
# SETUP
# ======================================================

async def setup(bot):

    await bot.add_cog(
        Leveling(bot)
    )
