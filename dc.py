import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

# ======================================================
# LOAD ENV
# ======================================================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ TOKEN missing in .env")

# ======================================================
# INTENTS
# ======================================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.guilds = True

# ======================================================
# BOT SETUP
# ======================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# ======================================================
# READY EVENT
# ======================================================

@bot.event
async def on_ready():

    print("=" * 50)
    print(f"✅ Logged in as {bot.user}")
    print("✅ Katalyst Bot Online")
    print("=" * 50)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Community Growth 🚀"
        )
    )

# ======================================================
# LOAD COGS
# ======================================================

async def load_cogs():

    cogs = [
        "cogs.utility",
        "cogs.onboarding",
        "cogs.leveling"
    ]

    for cog in cogs:

        try:

            await bot.load_extension(cog)

            print(f"✅ Loaded {cog}")

        except Exception as e:

            print(f"❌ Failed loading {cog}")
            print(e)

# ======================================================
# ERROR HANDLER
# ======================================================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

        await ctx.send(
            "❌ Unknown command."
        )

    elif isinstance(error, commands.MissingPermissions):

        await ctx.send(
            "❌ Missing permissions."
        )

    else:

        print(error)

# ======================================================
# START BOT
# ======================================================

async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)

asyncio.run(main())
