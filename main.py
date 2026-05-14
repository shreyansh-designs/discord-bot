import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

# ======================================================
# LOAD ENV VARIABLES
# ======================================================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ TOKEN missing in .env file")

# ======================================================
# DISCORD INTENTS
# ======================================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.guilds = True

# ======================================================
# BOT SETUP
# ======================================================

bot = commands.Bot(
    command_prefix="k!",
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# ======================================================
# READY EVENT
# ======================================================

@bot.event
async def on_ready():

    print("=" * 60)
    print(f"✅ Logged in as: {bot.user}")
    print(f"✅ Bot ID: {bot.user.id}")
    print(f"✅ Connected Servers: {len(bot.guilds)}")
    print("✅ KATALYST ONLINE")
    print("=" * 60)

    try:

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="k!helpme"
            )
        )

    except Exception as e:

        print(f"❌ Presence Error: {e}")

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

            print(f"✅ Loaded Cog: {cog}")

        except Exception as e:

            print("=" * 60)
            print(f"❌ Failed to load cog: {cog}")
            print(e)
            print("=" * 60)

# ======================================================
# BASIC TEST COMMAND
# ======================================================

@bot.command()
async def alive(ctx):

    embed = discord.Embed(
        title="✅ KATALYST ONLINE",
        description="Bot is working properly.",
        color=discord.Color.green()
    )

    await ctx.send(embed=embed)

# ======================================================
# GLOBAL ERROR HANDLER
# ======================================================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

        await ctx.send(
            "❌ Unknown command.\nUse `k!helpme`"
        )

    elif isinstance(error, commands.CommandOnCooldown):

        await ctx.send(
            f"⏳ Slow down.\nTry again in `{round(error.retry_after, 1)}s`"
        )

    elif isinstance(error, commands.MissingPermissions):

        await ctx.send(
            "❌ You don't have permission."
        )

    elif isinstance(error, commands.BotMissingPermissions):

        await ctx.send(
            "❌ Bot lacks required permissions."
        )

    else:

        print("=" * 60)
        print("❌ UNHANDLED ERROR")
        print(error)
        print("=" * 60)

        try:

            await ctx.send(
                "⚠️ Unexpected error occurred."
            )

        except:
            pass

# ======================================================
# STARTUP FUNCTION
# ======================================================

async def main():

    async with bot:

        await load_cogs()

        try:

            await bot.start(TOKEN)

        except discord.LoginFailure:

            print("❌ Invalid Discord Token")

        except Exception as e:

            print(f"❌ Fatal Startup Error: {e}")

# ======================================================
# RUN BOT
# ======================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("🛑 Bot stopped manually")

    except Exception as e:

        print(f"❌ Critical Error: {e}")
