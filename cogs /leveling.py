import discord
from discord.ext import commands
from collections import defaultdict
import json
import os

XP_FILE = "data/xp.json"

if not os.path.exists(XP_FILE):

    with open(XP_FILE, "w") as f:
        json.dump({}, f)

with open(XP_FILE, "r") as f:
    user_xp = json.load(f)

RANKS = {
    0: "🌱 New Joiner",
    100: "🧠 Novice",
    300: "⚡ Skilled",
    700: "🔥 Advanced",
    1200: "👑 Supreme",
    2000: "💎 Ultimate"
}

def save_xp():

    with open(XP_FILE, "w") as f:
        json.dump(user_xp, f)

def get_rank(xp):

    current = "🌱 New Joiner"

    for required, rank in RANKS.items():

        if xp >= required:
            current = rank

    return current

class Leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        user_id = str(message.author.id)

        if user_id not in user_xp:
            user_xp[user_id] = 0

        user_xp[user_id] += 5

        save_xp()

    @commands.command()
    async def profile(self, ctx):

        user_id = str(ctx.author.id)

        xp = user_xp.get(user_id, 0)

        rank = get_rank(xp)

        embed = discord.Embed(
            title=f"👤 {ctx.author.name}",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="⚡ XP",
            value=str(xp)
        )

        embed.add_field(
            name="🏆 Rank",
            value=rank
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):

        sorted_users = sorted(
            user_xp.items(),
            key=lambda x: x[1],
            reverse=True
        )

        embed = discord.Embed(
            title="🏆 Leaderboard",
            color=discord.Color.gold()
        )

        text = ""

        for index, (user_id, xp) in enumerate(sorted_users[:10], start=1):

            user = self.bot.get_user(
                int(user_id)
            )

            if user:

                text += (
                    f"{index}. "
                    f"{user.name} — "
                    f"{xp} XP — "
                    f"{get_rank(xp)}\n"
                )

        embed.description = text

        await ctx.send(embed=embed)

async def setup(bot):

    await bot.add_cog(
        Leveling(bot)
    )
